use anyhow::{Context, Result};
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::SampleFormat;
use hound;
use reqwest::blocking::Client;
use serde::Deserialize;
use simple_transcribe_rs::{model_handler, transcriber};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use tts::Tts;
use std::collections::HashMap;

#[derive(Deserialize)]
struct TextResponse {
    text: String,
}

// Speech-to-Text: Record audio, transcribe, print, and send to Flask
fn transcribe_and_send() -> Result<()> {
    // Set up audio capture with cpal
    let host = cpal::default_host();
    let device = host.default_input_device().context("No input device available")?;
    let config = device.default_input_config().context("Failed to get default input config")?;

    // Prepare a buffer to store audio data
    let audio_data: Arc<Mutex<Vec<i16>>> = Arc::new(Mutex::new(Vec::new()));

    // Capture params before moving config
    let channels = config.channels();
    let sample_rate = config.sample_rate().0;
    let sample_format = config.sample_format();
    let stream_config: cpal::StreamConfig = config.clone().into();

    // Build input stream depending on sample format
    let audio_data_clone = audio_data.clone();
    let stream = match sample_format {
        SampleFormat::F32 => {
            device.build_input_stream(
                &stream_config,
                move |data: &[f32], _: &cpal::InputCallbackInfo| {
                    let mut buffer = audio_data_clone.lock().unwrap();
                    // Convert f32 [-1.0, 1.0] to i16
                    buffer.extend(data.iter().map(|&s| {
                        let v = (s * i16::MAX as f32).round();
                        v.clamp(i16::MIN as f32, i16::MAX as f32) as i16
                    }));
                },
                |err| eprintln!("Error in stream: {}", err),
                None,
            )?
        }
        SampleFormat::I16 => {
            let audio_data_clone = audio_data.clone();
            device.build_input_stream(
                &stream_config,
                move |data: &[i16], _: &cpal::InputCallbackInfo| {
                    let mut buffer = audio_data_clone.lock().unwrap();
                    buffer.extend_from_slice(data);
                },
                |err| eprintln!("Error in stream: {}", err),
                None,
            )?
        }
        SampleFormat::U16 => {
            device.build_input_stream(
                &stream_config,
                move |data: &[u16], _: &cpal::InputCallbackInfo| {
                    let mut buffer = audio_data_clone.lock().unwrap();
                    // Convert unsigned to signed centered around 0
                    buffer.extend(data.iter().map(|&s| {
                        (s as i32 - i16::MAX as i32 - 1).clamp(i16::MIN as i32, i16::MAX as i32) as i16
                    }));
                },
                |err| eprintln!("Error in stream: {}", err),
                None,
            )?
        }
        _ => {
            // Fallback: attempt f32 path
            device.build_input_stream(
                &stream_config,
                move |data: &[f32], _: &cpal::InputCallbackInfo| {
                    let mut buffer = audio_data_clone.lock().unwrap();
                    buffer.extend(data.iter().map(|&s| {
                        let v = (s * i16::MAX as f32).round();
                        v.clamp(i16::MIN as f32, i16::MAX as f32) as i16
                    }));
                },
                |err| eprintln!("Error in stream: {}", err),
                None,
            )?
        }
    };

    // Start recording
    stream.play()?;
    println!("Recording for 5 seconds...");
    std::thread::sleep(Duration::from_secs(5));

    // Stop recording
    drop(stream);

    // Get recorded data
    let samples = audio_data.lock().unwrap().clone();

    // Write to WAV file
    let spec = hound::WavSpec {
        channels,
        sample_rate,
        bits_per_sample: 16,
        sample_format: hound::SampleFormat::Int,
    };

    let mut writer = hound::WavWriter::create("temp_recording.wav", spec)?;
    for sample in samples {
        writer.write_sample(sample)?;
    }

    writer.finalize()?;

    // Transcribe using simple_transcribe_rs
    let rt = tokio::runtime::Runtime::new().context("Failed to create Tokio runtime")?;
    let model = rt.block_on(model_handler::ModelHandler::new("tiny", "models/"));
    let trans = transcriber::Transcriber::new(model);
    let result = trans
        .transcribe("temp_recording.wav", None)
        .map_err(|e| anyhow::Error::msg(format!("Transcription failed: {}", e)))?;
    let text: String = result.get_text().to_string();
    println!("Transcribed text: {}", text);

    // Send to Flask server
    let client = Client::new();
    let mut map: HashMap<&str, String> = HashMap::new();
    map.insert("text", text.clone());
    let res = client
        .post("http://localhost:5000/transcription")
        .json(&map)
        .send()
        .context("Failed to send to Flask")?;
    println!("Server response: {:?}", res.status());

    // Clean up
    std::fs::remove_file("temp_recording.wav")?;

    Ok(())
}

// Text-to-Speech: Fetch text from Flask and speak
fn speak_text_from_flask(url: &str) -> Result<()> {
    // Fetch JSON from Flask server
    let response: TextResponse = reqwest::blocking::get(url)
        .context("Failed to fetch from Flask server")?
        .json()
        .context("Failed to parse JSON response")?;

    // Initialize TTS
    let mut tts = Tts::default().context("Failed to initialize TTS")?;

    // Speak the text (non-blocking)
    tts.speak(&response.text, false).context("Failed to speak text")?;

    Ok(())
}

fn main() -> Result<()> {
    // Parse command-line arguments
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        println!("Usage: {} [stt|tts]", args[0]);
        return Ok(());
    }

    match args[1].as_str() {
        "stt" => {
            println!("Running Speech-to-Text...");
            transcribe_and_send()
        }
        "tts" => {
            println!("Running Text-to-Speech...");
            speak_text_from_flask("http://localhost:5000/get_text")
        }
        _ => {
            println!("Invalid mode. Use 'stt' or 'tts'.");
            Ok(())
        }
    }
}