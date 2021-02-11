from serinda.plugin.OpenCVPlugin.filters.GridFilter import GridFilter
from serinda.plugin.OpenCVPlugin.filters.TimestampDisplayFilter import TimestampDisplayFilter
from serinda.plugin.OpenCVPlugin.old.MotionDetector import MotionDetector
from serinda.plugin.OpenCVPlugin.old.TrackObjectByGridPoints import TrackObjectByGridPoints
from serinda.plugin.OpenCVPlugin.filters.barcodedetect import BarcodeDetect
from serinda.plugin.OpenCVPlugin.filters.facedetection import FaceDetection
import cv2

class OpenCVPlugin:
    pluginList = [TimestampDisplayFilter(), GridFilter(), BarcodeDetect(), FaceDetection(), TrackObjectByGridPoints()]

    def __init__(self):
        self.detectMotion = False
        self.faceDetection = False
        self.barcodeDetection = False
        self.writeToFile = False
        self.timestamp = False
        self.showGrid = False
        self.trackObjectByGrid = False

        global out

    def processIntent(self, intent):
        return ["", ""]

    def processFilters(self, frame, params):
        params['showTimestamp'] = self.timestamp
        params['showGrid'] = self.showGrid
        params['showFaceDetection'] = self.faceDetection
        params['showBarcode'] = self.barcodeDetection
        params['detectMotion'] = self.detectMotion
        params['writeToFile'] = self.writeToFile
        params['trackObjectByGrid'] = self.trackObjectByGrid

        for i in self.pluginList:
            frame = i.processFilter(frame, params)

        if params['writeToFile']:
            self.out.write(frame)

        MotionDetector(params).processFilter(frame, params)

        return frame

    def setCommand(self, cmd):
        # eventually I want this to parse as below so we can get all of the information out of the intent
        command = cmd['intent']['intentName']
        if command == 'detectMotion':
            self.detectMotion = not self.detectMotion
        elif command == 'faceDetect':
            self.faceDetection = not self.faceDetection
        elif command == 'detectBarcode':
            self.barcodeDetection = not self.barcodeDetection
        elif command == 'recordVideo':
            if self.writeToFile:
                self.out.release()
            else:
                frame_width = 640
                frame_height = 480
                fileName = 'outpy.avi'
                self.out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

            self.writeToFile = not self.writeToFile
        elif command == "timestamp":
            self.timestamp = not self.timestamp
        elif command == "showGrid":
            self.showGrid = not self.showGrid
        elif command == "trackObjectByGrid":
            self.trackObjectByGrid = not self.trackObjectByGrid
