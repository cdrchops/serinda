from flask import Flask, jsonify, Response, render_template
import speech_recognition as sr
import threading
import time
import argparse
import cv2
import numpy as np
import os
# import mediapipe as mp

app = Flask(__name__)
app.config['DEBUG'] = False

# Initialize the recognizer
recognizer = sr.Recognizer()

# # Initialize Mediapipe Hand solution
# mp_hands = mp.solutions.hands
#
# hands = mp_hands.Hands(static_image_mode=False,
#                        max_num_hands=2,
#                        min_detection_confidence=0.1,
#                        min_tracking_confidence=0.1)
#
# mp_drawing = mp.solutions.drawing_utils

# Global variables
RECOGNIZER_TYPE = None
LATEST_RESULT = {"status": "none", "message": "No speech processed yet"}
LATEST_FACES = []  # Store latest face coordinates
LATEST_HANDS = []  # Store latest hand landmarks
LOCK = threading.Lock()
WAKE_WORD = "hey flask"
CAMERA = cv2.VideoCapture(0)  # Initialize webcam
DEBUG = False

# Initialize Haar cascade for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    cascade_path = 'haarcascade_frontalface_default.xml'  # Fallback to local file
FACE_CASCADE = cv2.CascadeClassifier(cascade_path)
if FACE_CASCADE.empty():
    raise RuntimeError("Failed to load Haar cascade file")


def debug(msg):
    if DEBUG:
        print(msg)


# Function to recognize speech
def recognize_speech(audio):
    try:
        debug("Processing...")
        if RECOGNIZER_TYPE == "sphinx":
            text = recognizer.recognize_sphinx(audio)
        else:
            text = recognizer.recognize_google(audio)
        return {"status": "success", "text": text}
    except sr.UnknownValueError:
        return {"status": "error", "message": "Could not understand the audio"}
    except sr.RequestError as e:
        return {"status": "error", "message": f"Speech recognition service error: {str(e)}"}


# Function for continuous wake word detection and audio recording
def audio_listener():
    global LATEST_RESULT
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                debug(f"Listening for wake word '{WAKE_WORD}'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                try:
                    if RECOGNIZER_TYPE == "sphinx":
                        text = recognizer.recognize_sphinx(audio).lower()
                    else:
                        text = recognizer.recognize_google(audio).lower()
                    if WAKE_WORD.lower() in text:
                        debug("Wake word detected! Recording...")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        debug("Listening for command...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        result = recognize_speech(audio)
                        with LOCK:
                            LATEST_RESULT = result
                    else:
                        debug(f"No wake word detected in: {text}")
                except sr.UnknownValueError:
                    debug("Could not understand audio for wake word")
                except sr.RequestError as e:
                    debug(f"Wake word detection error: {str(e)}")
            except sr.WaitTimeoutError:
                debug("No audio detected for wake word")
            except Exception as e:
                debug(f"Error in audio listener: {str(e)}")
                with LOCK:
                    LATEST_RESULT = {"status": "error", "message": f"Audio listener error: {str(e)}"}
            time.sleep(0.1)  # Prevent excessive CPU usage


# Function to generate video frames with face and hand detection
def generate_frames():
    global LATEST_FACES, LATEST_HANDS
    while True:
        success, frame = CAMERA.read()
        if not success:
            break
        else:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Update face coordinates
            with LOCK:
                LATEST_FACES = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces]

            # Draw bounding boxes for faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # Process the RGB frame with MediaPipe Hands
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # results = hands.process(frame_rgb)
            #
            # # Update hand landmarks
            # hand_data = []
            # if results.multi_hand_landmarks:
            #     for hand_landmarks in results.multi_hand_landmarks:
            #         landmarks = []
            #         for lm in hand_landmarks.landmark:
            #             h, w, _ = frame.shape
            #             cx, cy = int(lm.x * w), int(lm.y * h)  # Convert to pixel coordinates
            #             landmarks.append({"x": cx, "y": cy, "z": lm.z})
            #         hand_data.append({"landmarks": landmarks})
            #         mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            #
            # with LOCK:
            #     LATEST_HANDS = hand_data

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(0.033)  # Approx 30 FPS


# Flask route for index page
@app.route('/')
def index():
    return render_template('index.html')


# Flask route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Flask route for face coordinates
@app.route('/face_data', methods=['GET'])
def face_data():
    with LOCK:
        return jsonify({"faces": LATEST_FACES})


# Flask route for hand landmarks
@app.route('/hand_data', methods=['GET'])
def hand_data():
    with LOCK:
        return jsonify({"hands": LATEST_HANDS})


# Flask route to get latest transcription
@app.route('/recognize', methods=['GET'])
def speech_to_text():
    with LOCK:
        return jsonify(LATEST_RESULT)


# Flask route to check recognizer type
@app.route('/recognizer', methods=['GET'])
def get_recognizer():
    return jsonify({"recognizer": RECOGNIZER_TYPE})


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Flask Speech Recognition and Video Streaming Server")
    parser.add_argument('--recognizer', choices=['google', 'sphinx'], default='google',
                        help="Speech recognizer to use (google or sphinx)")
    args = parser.parse_args()

    # Set the recognizer type
    RECOGNIZER_TYPE = args.recognizer
    debug(f"Starting server with {RECOGNIZER_TYPE} recognizer")

    # Start the audio listener in a background thread
    listener_thread = threading.Thread(target=audio_listener, daemon=True)
    listener_thread.start()

    # Start the Flask server
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_debugger=False, threaded=True)
    finally:
        CAMERA.release()
        # hands.close()