from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import cv2
import numpy as np
import asyncio

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
pcs = set()  # Store peer connections

class DepthTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.disparity = None

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        if self.disparity is not None:
            # Convert grayscale disparity to BGR for video frame
            frame = cv2.cvtColor(self.disparity, cv2.COLOR_GRAY2BGR)
            video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
            video_frame.pts = pts
            video_frame.time_base = time_base
            return video_frame
        else:
            # Return a blank frame if no disparity yet
            blank = np.zeros((480, 640, 3), dtype=np.uint8)
            video_frame = VideoFrame.from_ndarray(blank, format="bgr24")
            video_frame.pts = pts
            video_frame.time_base = time_base
            return video_frame

async def process_frames(track, output_queue):
    while True:
        frame = await track.recv()  # Receive video frame
        img = frame.to_ndarray(format="bgr24")
        output_queue.append(img)  # Store frame for processing

@socketio.on('offer')
async def handle_offer(data):
    offer = RTCSessionDescription(sdp=data['sdp'], type=data['type'])
    pc = RTCPeerConnection()
    pcs.add(pc)
    frames1 = []
    frames2 = []
    depth_track = DepthTrack()
    pc.addTrack(depth_track)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            if not frames1:
                asyncio.ensure_future(process_frames(track, frames1))
            else:
                asyncio.ensure_future(process_frames(track, frames2))

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    emit('answer', {'sdp': pc.localDescription.sdp, 'type': pc.localDescription.type})

    # Process depth when two frames are available
    while True:
        if frames1 and frames2:
            frame1, frame2 = frames1.pop(0), frames2.pop(0)
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
            disparity = stereo.compute(gray1, gray2)
            # Normalize for visualization
            disparity = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_track.disparity = disparity
        await asyncio.sleep(0.033)  # ~30 FPS

@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    emit('ice-candidate', data, broadcast=True)  # For simple 1:1 setup

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)