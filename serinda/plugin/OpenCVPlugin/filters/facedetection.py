import cv2

class FaceDetection:

    def __init__(self):
        # todo: fix path so it's relative to the project and not an absolute path
        # todo: add more pretrained models
        self.face_cascade = cv2.CascadeClassifier('./pretrained_models/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('./pretrained_models/haarcascade_eye.xml')

    def detect_face(self, transparent_img, img):
        face_img = img.copy()
        #  face_rects = face_cascade.detectMultiScale(face_img)
        face_rects = self.face_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 255, 0, 255), 2)

        return (transparent_img, face_img)

    def detect_eye(self, transparent_img, img):
        face_img = img.copy()
        eyes_rects = self.eye_cascade.detectMultiScale(face_img, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in eyes_rects:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 255, 0, 255), 2)

        return (transparent_img, face_img)

    def processFilter(self, transparent_img, frame, params):
        # if params['showFaceDetection']:
        (transparent_img, frame) = self.detect_face(transparent_img, frame)

        # todo: add more detections here so it won't just be one eye, but other features as well
        # (transparent_img, frame) = self.detect_eye(transparent_img, frame)

        return (transparent_img, frame)
