import cv2
# import imutils
# from imutils.video import VideoStream
import numpy as np
import os

# face_cascade = cv2.CascadeClassifier(os.path.join("pretrained_models", "haarcascade_frontalface_alt2.xml"))
ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)
        # self.vs = VideoStream(src=1).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        # h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print("width")
        # print(w)
        # print("height")
        # print(h)
        # image = self.vs.read()
        # image = imutils.resize(image, width=800)
        # transparent_img = np.zeros((1280, 800, 4), dtype=np.uint8)
        # transparent_img = np.zeros((640, 480, 4), dtype=np.uint8)
        # image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        # return face_rects
        # for (x, y, w, h) in face_rects:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 255, 0, 255), 2)
        #     break

        ret, jpeg = cv2.imencode('.png', image)
        return (jpeg.tobytes())#, face_rects)
