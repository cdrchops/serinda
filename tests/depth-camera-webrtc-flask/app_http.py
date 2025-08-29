from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import base64
from io import BytesIO
import time

app = Flask(__name__)

def compute_depth(frame1, frame2):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(gray1, gray2)
    disparity = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return disparity

disparity_queue = []  # Store processed disparity for streaming

@app.route('/')
def index():
    return render_template('index_http.html')  # Use a variant of index.html with HTTP JS

@app.route('/process_frames', methods=['POST'])
def process_frames():
    data = request.json
    frame1_data = base64.b64decode(data['frame1'].split(',')[1])
    frame2_data = base64.b64decode(data['frame2'].split(',')[1])
    frame1 = cv2.imdecode(np.frombuffer(frame1_data, np.uint8), cv2.IMREAD_COLOR)
    frame2 = cv2.imdecode(np.frombuffer(frame2_data, np.uint8), cv2.IMREAD_COLOR)
    disparity = compute_depth(frame1, frame2)
    disparity_queue.append(disparity)
    return {'status': 'processed'}

def generate_disparity_stream():
    while True:
        if disparity_queue:
            disparity = disparity_queue.pop(0)
            ret, buffer = cv2.imencode('.jpg', disparity)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.033)  # ~30 FPS

@app.route('/disparity_stream')
def disparity_stream():
    return Response(generate_disparity_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)