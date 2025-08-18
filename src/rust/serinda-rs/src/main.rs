use std::path::Path;
use std::sync::{Arc, Mutex};
use std::time::Duration;
use std::thread;

use anyhow::{anyhow, Result};
use clap::Parser;
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use vosk::{Model, Recognizer};
use tts::Tts;
use actix_web::{post, web, App, HttpResponse, HttpServer, Responder};
use reqwest;
use serde::{Deserialize, Serialize};
use tokio::sync::mpsc;

#[derive(Parser, Debug)]
struct Args {
    #[arg(long)]
    server_mode: bool,

    #[arg(long, default_value = "http://127.0.0.1:5000/process")]
    flask_url: String,

    #[arg(long, default_value = "./models/vosk_model")]
    vosk_path: String,

    #[arg(long, default_value = "./models/vosk_small_model")]
    wake_model: String,

    #[arg(long, default_value = "hey grok")]
    wake_word: String,
}

#[derive(Serialize, Deserialize)]
struct ProcessRequest {
    text: String,
}

#[derive(Serialize, Deserialize)]
struct IntentResponse {
    intent: String,
}

#[derive(Serialize, Deserialize)]
struct FlaskRequest {
    intent: String,
}

#[derive(Serialize, Deserialize)]
struct FlaskResponse {
    response: String,
}

async fn get_intent_from_flask(text: &str, flask_url: &str) -> Result<String> {
    let client = reqwest::Client::new();
    let resp = client
        .post(flask_url)
        .json(&ProcessRequest { text: text.to_string() })
        .send()
        .await
        .map_err(|e| anyhow!("Flask request error: {}", e))?;

    let flask_res = resp
        .json::<IntentResponse>()
        .await
        .map_err(|e| anyhow!("Flask response parse error: {}", e))?;

    Ok(flask_res.intent)
}

#[post("/process")]
async fn process_text(
    body: web::Json<ProcessRequest>,
    data: web::Data<AppData>,
) -> impl Responder {
    match get_intent_from_flask(&body.text, &data.flask_url).await {
        Ok(intent) => {
            let client = reqwest::Client::new();
            match client
                .post(&data.flask_url)
                .json(&FlaskRequest {
                    intent: intent.clone(),
                })
                .send()
                .await
            {
                Ok(resp) => match resp.json::<FlaskResponse>().await {
                    Ok(flask_res) => {
                        if let Err(e) = play_tts(&data.tts, &flask_res.response) {
                            log::error!("TTS error: {}", e);
                            HttpResponse::InternalServerError().body("TTS playback failed")
                        } else {
                            HttpResponse::Ok().json(IntentResponse { intent })
                        }
                    }
                    Err(e) => {
                        log::error!("Flask response error: {}", e);
                        HttpResponse::InternalServerError().body(format!("Flask response error: {}", e))
                    }
                },
                Err(e) => {
                    log::error!("Flask request error: {}", e);
                    HttpResponse::InternalServerError().body(format!("Flask request error: {}", e))
                }
            }
        }
        Err(e) => {
            log::error!("Flask intent error: {}", e);
            HttpResponse::InternalServerError().body(format!("Flask intent error: {}", e))
        }
    }
}

#[post("/speak")]
async fn speak_BlackJack_speak_text(
body: web::Json<ProcessRequest>,
data: web::Data<AppData>,
) -> impl Responder {
    match play_tts(&data.tts, &body.text) {
    Ok(_) => HttpResponse::Ok().body("Spoken"),
    Err(e) => {
    log::error!("TTS error: {}", e);
    HttpResponse::InternalServerError().body(format!("TTS error: {}", e))
    }
    }
}

struct AppData {
    tts: Tts,
    flask_url: String,
}

fn play_tts(tts: &Tts, text: &str) -> Result<()> {
    tts.speak(text, false).map_err(|e| anyhow!("TTS error: {}", e))?;
    Ok(())
}

#[derive(Clone)]
enum ListenState {
    Wake,
    Command,
}

async fn run_server(app_data: AppData) -> Result<()> {
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(app_data.clone()))
            .service(process_text)
            .service(speak_text)
    })
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
        .map_err(|e| anyhow!("Server error: {}", e))?;
    Ok(())
}

fn run_audio_loop(
    args: Args,
    tts: Tts,
    shutdown_rx: mpsc::Receiver<()>,
) -> Result<()> {
    let wake_model = Model::new(&args.wake_model)?;
    let full_model = Model::new(&args.vosk_path)?;

    let host = cpal::default_host();
    let device = host.default_input_device().ok_or(anyhow!("No input device"))?;
    let config = device.default_input_config()?;

    let sample_rate = config.sample_rate().0 as f32;
    let channels = config.channels();

    if channels != 1 {
        return Err(anyhow!("Only mono input supported"));
    }

    if config.sample_format() != cpal::SampleFormat::F32 {
        return Err(anyhow!("Only f32 samples supported"));
    }

    let grammar = format!(r#"["{}"]"#, args.wake_word);
    let wake_rec_base = Recognizer::new_with_grammar(&wake_model, sample_rate, &grammar)?;

    let state = Arc::new(Mutex::new(ListenState::Wake));
    let wake_rec = Arc::new(Mutex::new(wake_rec_base));
    let full_rec: Arc<Mutex<Option<Recognizer>>> = Arc::new(Mutex::new(None));
    let tts = Arc::new(Mutex::new(tts));

    let flask_url = args.flask_url.clone();
    let wake_word = args.wake_word.clone();

    let err_fn = |err| log::error!("Stream error: {}", err);

    let stream = device.build_input_stream(
        &config.into(),
        move |data: &[f32], _: &cpal::InputCallbackInfo| {
            let audio_i16: Vec<i16> = data
                .iter()
                .map(|&s| (s.clamp(-1.0, 1.0) * 32767.0) as i16)
                .collect();

            let current_state = state.lock().unwrap_or_else(|e| {
                log::error!("Mutex poisoned: {}", e);
                ListenState::Wake
            });

            match current_state {
                ListenState::Wake => {
                    let mut wr = wake_rec.lock().unwrap_or_else(|e| {
                        log::error!("Mutex poisoned: {}", e);
                        panic!("Recognizer mutex poisoned");
                    });
                    if wr.accept_waveform(&audio_i16) {
                        if let Ok(res) = wr.result() {
                            if res.text.trim().to_lowercase() == wake_word.to_lowercase() {
                                log::info!("Wake word detected: {}", wake_word);
                                let mut s = state.lock().unwrap_or_else(|e| {
                                    log::error!("Mutex poisoned: {}", e);
                                    panic!("State mutex poisoned");
                                });
                                *s = ListenState::Command;
                                let mut fr = full_rec.lock().unwrap_or_else(|e| {
                                    log::error!("Mutex poisoned: {}", e);
                                    panic!("Recognizer mutex poisoned");
                                });
                                if let Ok(new_rec) = Recognizer::new(&full_model, sample_rate) {
                                    *fr = Some(new_rec);
                                } else {
                                    log::error!("Failed to create full recognizer");
                                }
                            }
                        }
                    }
                }
                ListenState::Command => {
                    let mut fr_opt = full_rec.lock().unwrap_or_else(|e| {
                        log::error!("Mutex poisoned: {}", e);
                        panic!("Recognizer mutex poisoned");
                    });
                    if let Some(ref mut rec) = *fr_opt {
                        if rec.accept_waveform(&audio_i16) {
                            if let Ok(res) = rec.final_result() {
                                if !res.text.is_empty() {
                                    log::info!("Recognized command: {}", res.text);

                                    // Spawn async task to handle Flask requests
                                    let flask_url = flask_url.clone();
                                    let tts = Arc::clone(&tts);
                                    let state = Arc::clone(&state);
                                    let full_rec = Arc::clone(&full_rec);
                                    let text = res.text.to_string();

                                    tokio::spawn(async move {
                                        let client = reqwest::Client::new();
                                        match get_intent_from_flask(&text, &flask_url).await {
                                            Ok(intent) => {
                                                match client
                                                    .post(&flask_url)
                                                    .json(&FlaskRequest { intent })
                                                    .send()
                                                    .await
                                                {
                                                    Ok(resp) => match resp.json::<FlaskResponse>().await {
                                                        Ok(flask_res) => {
                                                            let tts = tts.lock().unwrap_or_else(|e| {
                                                                log::error!("Mutex poisoned: {}", e);
                                                                panic!("TTS mutex poisoned");
                                                            });
                                                            if let Err(e) = play_tts(&tts, &flask_res.response) {
                                                                log::error!("TTS error: {}", e);
                                                            }
                                                        }
                                                        Err(e) => log::error!("Flask response error: {}", e),
                                                    },
                                                    Err(e) => log::error!("Flask request error: {}", e),
                                                }
                                            }
                                            Err(e) => log::error!("Flask intent error: {}", e),
                                        }

                                        let mut s = state.lock().unwrap_or_else(|e| {
                                            log::error!("Mutex poisoned: {}", e);
                                            panic!("State mutex poisoned");
                                        });
                                        *s = ListenState::Wake;
                                        let mut fr = full_rec.lock().unwrap_or_else(|e| {
                                            log::error!("Mutex poisoned: {}", e);
                                            panic!("Recognizer mutex poisoned");
                                        });
                                        *fr = None;
                                    });
                                }
                            }
                        }
                    }
                }
            }
        },
        err_fn,
        Some(Duration::from_secs(300)),
    )?;

    stream.play()?;
    shutdown_rx.blocking_recv().ok_or(anyhow!("Shutdown signal received"))?;
    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    env_logger::init();

    let args = Args::parse();
    let tts = Tts::default().map_err(|e| anyhow!("TTS init error: {}", e))?;

    if args.server_mode {
        let app_data = AppData {
            tts,
            flask_url: args.flask_url,
        };
        run_server(app_data).await
    } else {
        let (shutdown_tx, shutdown_rx) = mpsc::channel::<()>(1);
        let result = run_audio_loop(args, tts, shutdown_rx);

        // Allow graceful shutdown with Ctrl+C
        ctrlc::set_handler(move || {
            log::info!("Received shutdown signal");
            shutdown_tx.blocking_send(()).unwrap();
        })
            .map_err(|e| anyhow!("Ctrl+C handler error: {}", e))?;

        result
    }
}