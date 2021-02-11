import cv2
import numpy as np
# from imutils.video import VideoStream

face_cascade=cv2.CascadeClassifier("../../pretrained_models/haarcascade_frontalface_alt2.xml")
ds_factor=1 # was 0.6


class VideoCamera(object):
    filters = dict()
    cameraNumber = 0
    params = {}

    def __init__(self, camNumber, picam=False):
        self.cameraNumber = camNumber
        if picam:
            print("is picam")
            # self.vs = VideoStream(usePiCamera=1)
        else:
            # self.vs = VideoStream(src=camNumber)
            self.video = cv2.VideoCapture(camNumber)
    
    def __del__(self):
        self.video.release()

    def generate(self):
        while True:
            frame = self.get_frame()
            
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield ("error")

    def get_frame(self):
        success, frame = self.video.read()
        if frame is not None and frame.shape is not None:  # TODO: and success is True ?????
            # transparent_img = np.zeros((frame.shape[0], frame.shape[1], 4), dtype=np.uint8)
            # This works for the size of the view screen I have - this may have to be different for other view screens
            # TODO: put this as a configuration in the props file - the height and width of the transparent image
            # transparent_img = np.zeros((320, 370, 4), dtype=np.uint8)
            # transparent_img = np.zeros((640, 480, 4), dtype=np.uint8)
            transparent_img = np.zeros((1280, 800, 4), dtype=np.uint8)
            frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
            # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # face_rects = face_cascade.detectMultiScale(gray,1.3,5)
            # for (x, y, w, h) in face_rects:
            #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #     cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 255, 0, 255), 2)
            #     break

            # https://codeburst.io/filtering-dictionary-in-python-3-3eb99f92e6ee
            # to cover the dictionary changed during iteration - passing the shallow copy {**self.filters} fixes it
            # if we want to send back just the processed item we need to return the transparent_image
            # if we want to send back the processed image then we just send back the frame
            if True:
                return self.process({**self.filters}, transparent_img, frame, ".png", self.params)
            else:
                return self.process({**self.filters}, frame, frame, ".jpg", self.params)

    def process(self, filtr, transparent_img, image, encode, params):
        for filterz in filtr.values():
            (transparent_img, face_img) = filterz.processFilter(transparent_img, image, params)

        ret, encodedImage = cv2.imencode(encode, transparent_img)
        return encodedImage.tobytes()

    def addFilter(self, filterName, filter):
        if self.filters.get(filterName) == None:
            self.filters[filterName] = filter

    def removeFilter(self, filterName):
        if self.filters.get(filterName) != None:
            self.filters.pop(filterName)

