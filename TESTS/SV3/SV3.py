# Required libraries
import speech_recognition as sr
import pyttsx3
import requests
from flask import Flask, request, render_template
import threading
import time

from SpeechRec import SpeechRec

# Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Snips Mockup (replace this with actual Snips integration)
def get_intent_from_snips(command):
    # Mock intent extraction
    return command.replace(" ", "_").lower()

# Flask Application
app = Flask(__name__)
command_result = ""

@app.route('/')
def index():
    return render_template('index.html', result=command_result)

@app.route('/cmd')
def handle_command():
    global command_result
    intent = request.args.get('cmd')
    # Business logic placeholder
    command_result = f"Processed intent: {intent}"
    print(command_result)
    return "hello world"

# Function to handle voice commands
def listen_for_commands():
     while True:
        print("Listening for wake word...")
        text = SpeechRec().record()

        if "hey paige" in text: # if text.count(self.WAKE) > 0:
            print("Wake word detected. Listening for command...")
            text = SpeechRec().record()

            print(f"Command received: {text}")

            response = requests.get(f"http://localhost:5000/cmd?cmd=this command")

            # Speak response
            speak(response.text)


if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()

    # Start listening for commands
    listen_for_commands()
