import moviepy.editor as mp 
import speech_recognition as sr 
from pydub import AudioSegment

fileNameVideo = "childbirth.mp4"
fileNameWav = "childbirth.wav"

# Load the video
video = mp.VideoFileClip(fileNameVideo)

# Extract the audio from the video
audio_file = video.audio
audio_file.write_audiofile(fileNameWav)

# Initialize recognizer
r = sr.Recognizer()

# https://stackoverflow.com/questions/62719408/speech-recognition-python-having-strange-request-error
# chunk the audio into smaller pieces
def chunk_audio_and_save(audio_path, chunk_length=60000):  # chunk_length in milliseconds
    audio = AudioSegment.from_wav(audio_path)
    length_audio = len(audio)
    chunk_paths = []
    for i, chunk in enumerate(range(0, length_audio, chunk_length)):
        chunk_audio = audio[chunk:chunk + chunk_length]
        chunk_path = f"temp_chunk_{i}.wav"
        chunk_audio.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

chunk_file_paths = chunk_audio_and_save(fileNameWav)

# https://stackoverflow.com/questions/48959098/how-to-create-a-new-text-file-using-python
# Method 1
f = open("./transcript.txt", "a")   # 'r' for reading and 'w' for writing
# f.write("Hello World from " + f.name)    # Write inside file
# f.close()                                # Close file

# Method 2
# with open("Path/To/Your/File.txt", "w") as f:   # Opens file and casts as f
#     f.write("Hello World form " + f.name)       # Writing
    # File closed automatically


for i, file_path in enumerate(chunk_file_paths):
    print(f"Transcribing chunk {i+1}/{len(chunk_file_paths)}...")

    # Load the audio file
    with sr.AudioFile(file_path) as source:
        data = r.record(source)

    # Convert speech to text
    text = r.recognize_google(data, language='en-US')

    # transcript = transcribe_audio(file_path)
    # full_transcript.append(text)
    f.write(text + "\n")  # Write inside file
    # os.remove(file_path)  # Clean up chunk file

    # Print the text
    print("\nThe resultant text from video is: \n")
    print(text)
