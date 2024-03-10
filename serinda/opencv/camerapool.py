# from serinda.opencv.camera import Camera
from serinda.opencv.DrawGrid import DrawGrid
from serinda.opencv.videocamera import VideoCamera
from serinda.plugin.OpenCVPlugin.filters.TimestampDisplayFilter import TimestampDisplayFilter
from serinda.plugin.OpenCVPlugin.filters.barcodedetect import BarcodeDetect
from serinda.plugin.OpenCVPlugin.filters.facedetection import FaceDetection

# import inspect module
import inspect

class CameraPool:
    cameras = []
    detectFaces = False
    showTimestamp = False
    trackObjectByGrid = False
    detectBarcode = False
    drawGrid = False
    detectMotion = False
    params = {}

    def __init__(self, propertiesFile):
        self.runCameras = propertiesFile.get("run.cameras")
        self.runCameras = self.runCameras == "True"

        self.numberOfCameras = int(propertiesFile.get("number.of.cameras"))
        print(str(self.numberOfCameras))
        singleCamera = propertiesFile.get("useSingleCamera")

        if singleCamera:
            self.createCamera("cam1", 1)
        else:
            for i in range(self.numberOfCameras):
                print("Camera ", str(i))
                self.createCamera("cam" + str(i), i)

    # TODO: cameraName is unused at this time but in the future could be used to identify a camera
    # TODO: add support for picam - to change False to True for picam
    def createCamera(self, cameraName, cameraNumber):
        camera = VideoCamera(cameraNumber, False)
        # print("creating camera " +str(cameraNumber))
        self.cameras.append(camera)

    # to give all cameras the same command
    def setCommand(self, command, nluIntentProcessor):
        intent = command
        tmpCamNumber = intent['slots'][0]['rawValue']

        print("intent camera number ", tmpCamNumber)

        intentName = nluIntentProcessor.getIntentNameByRecognition(intent)
        cameraNumber = int(tmpCamNumber) - 1 #intent[0].entities[0].value - 1
        cam = self.cameras[cameraNumber]

        if intentName == 'showGrid':
            self.drawGrid = not self.drawGrid

            if self.drawGrid:
                # cameras are in a zero based index so subtract one to get the actual camera number
                cam.addFilter('drawGrid', DrawGrid())
            else:
                cam.removeFilter('drawGrid')
        elif intentName == 'detectFaces':
            self.detectFaces = not self.detectFaces

            if self.detectFaces:
                cam.addFilter('detectFaces', FaceDetection())
            else:
                cam.removeFilter('detectFaces')
        elif intentName == 'showTimestamp':
            self.showTimestamp = not self.showTimestamp

            if self.showTimestamp:
                cam.addFilter('showTimestamp', TimestampDisplayFilter())
            else:
                cam.removeFilter('showTimestamp')
        elif intentName == 'trackObjectByGrid':
            self.trackObjectByGrid = not self.trackObjectByGrid

            # need to fix params pass through
            # if self.trackObjectByGrid:
                # wire this from the pool - somehow set this up so params are passed around as needed
                # self.params['gridX'] = 150
                # self.params['gridY'] = 150
                # self.params['sizeOfArea'] = 50
                # need to get these values from the request then delete them and use whatever's in track object by grid points
                # cam.addFilter('trackObjectByGrid', TrackObjectByGridPoints(self.params))
                # self.params = {}
            # else:
            #     cam.removeFilter('trackObjectByGrid')
        elif intentName == 'detectBarcode':
            self.detectBarcode = not self.detectBarcode

            if self.detectBarcode:
                cam.addFilter('detectBarcode', BarcodeDetect())
            else:
                cam.removeFilter('detectBarcode')
        elif intentName == 'detectMotion':
            self.detectMotion = not self.detectMotion
            #
            # if self.detectMotion:
            #     cam.addFilter('detectMotion', MotionDetector())
            # else:
            #     cam.removeFilter('detectMotion')

    # to give a singular camera a command
    def setCommandOnCamera(self, command, cameraNumber):
        self.cameras[cameraNumber].setCommand(command)

    def getCamera(self, cameraNumber):
        # print('get camera number ' + str(cameraNumber))
        # print(str(len(self.cameras)))
        # print(type(self.cameras[c]))
        tmpCam = self.cameras[cameraNumber]
        return tmpCam # .generate()

    # to start all cameras
    def start(self):
        for i in self.cameras:
            i.start()

    # to start a specific camera
    def startCamera(self, args, cameraNumber):
        self.cameras[cameraNumber].start(args)

    # to stop all cameras
    def stop(self):
        for i in self.cameras:
            i.stop()

    # to stop a single camera
    def stopCamera(self, cameraNumber):
        self.cameras[cameraNumber].stop()
