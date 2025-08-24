import cv2
import numpy as np
import os
# from imutils.video import VideoStream
import depthai as dai
import blobconverter

face_cascade=cv2.CascadeClassifier(os.path.join("pretrained_models", "haarcascade_frontalface_alt2.xml"))
ds_factor=1 # was 0.6

showVideo=False #as opposed to just black - you can view the video to see that it's calibrating correctly
class VideoCameraDepthAI(object):
    pipeline = dai.Pipeline()

    filters = dict()
    cameraNumber = 0
    params = {}
    def __init__(self, camNumber, picam=False):
        self.cameraNumber = camNumber

        # Create the ColorCamera node and set its properties
        camRgb = self.pipeline.create(dai.node.ColorCamera)
        camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

        # Create the XLinkOut node for the video stream and set its properties
        xoutRgb = self.pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("My first stream")

        # Link the ColorCamera to the XLinkOut node
        camRgb.video.link(xoutRgb.input)

    def __del__(self):
        print("delete video camera release")
        # self.video.release()

    def generate(self):
        # Start the pipeline
        with dai.Device(self.pipeline) as device:
            video_queue = device.getOutputQueue(name="My first stream", maxSize=4, blocking=False)  # get the video stream queue

            while True:
                frame = video_queue.get().getCvFrame()  # get the video frame as a numpy array

                transparent_img = np.zeros((1280, 800, 4), dtype=np.uint8)
                # transparent_img = np.zeros((300, 300, 4), dtype=np.uint8)

                if showVideo:
                    flag, frame = self.process({**self.filters}, transparent_img, frame, ".png", self.params)
                else:
                    flag, frame = self.process({**self.filters}, frame, frame, ".jpg", self.params)

                # if the frame was not successfully encoded, then skip this iteration
                if not flag:
                    continue

                if showVideo:
                    yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')
                else:
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

    def frameNorm(self, frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def process(self, filtr, transparent_img, image, encode, params):
        for filterz in filtr.values():
            (transparent_img, face_img) = filterz.processFilter(transparent_img, image, params)

        (flag, encodedImage) = cv2.imencode(encode, transparent_img)

        return flag, encodedImage

    def addFilter(self, filterName, filter):
        if self.filters.get(filterName) == None:
            self.filters[filterName] = filter

    def removeFilter(self, filterName):
        if self.filters.get(filterName) != None:
            self.filters.pop(filterName)

    def thing(self):
        # Pipeline is now finished, and we need to find an available device to run our pipeline
        # we are using context manager here that will dispose the device after we stop using it
        with dai.Device(self.pipeline) as device:
            # From this point, the Device will be in "running" mode and will start sending data via XLink

            # Define sources and outputs
            # imu = self.pipeline.create(dai.node.IMU)
            #
            # imuType = device.getConnectedIMU()
            # imuFirmwareVersion = device.getIMUFirmwareVersion()
            # embeddedIMUFirmwareVersion = device.getEmbeddedIMUFirmwareVersion()
            # print("IMU type " + imuType)
            # print("IMU embeddedIMUFirmwareVersion " + str(embeddedIMUFirmwareVersion))
            # print("IMU imuFirmwareVersion " + str(imuFirmwareVersion))

            #only if firmware needs to be updated
            # imu.enableFirmwareUpdate(True)
            # device.startIMUFirmwareUpdate()

            # To consume the device results, we get two output queues from the device, with stream names we assigned earlier
            q_rgb = device.getOutputQueue("rgb")
            # q_nn = device.getOutputQueue("nn")

            # Here, some of the default values are defined. Frame will be an image from "rgb" stream, detections will contain nn results
            frame = None
            # detections = []

            # Since the detections returned by nn have values from <0..1> range, they need to be multiplied by frame width/height to
            # receive the actual position of the bounding box on the image

            # Main host-side application loop
            while True:
                # we try to fetch the data from nn/rgb queues. tryGet will return either the data packet or None if there isn't any
                in_rgb = q_rgb.tryGet()
                # in_nn = q_nn.tryGet()
                #
                if in_rgb is not None:
                #     # If the packet from RGB camera is present, we're retrieving the frame in OpenCV format using getCvFrame
                    frame = in_rgb.getCvFrame()
                #
                # if in_nn is not None:
                #     # when data from nn is received, we take the detections array that contains mobilenet-ssd results
                #     detections = in_nn.detections

                if frame is not None:
                    # for detection in detections:
                    #     # for each bounding box, we first normalize it to match the frame size
                    #     bbox = self.frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                    #     # and then draw a rectangle on the frame to show the actual result
                    #     cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)

                    transparent_img = np.zeros((1280, 800, 4), dtype=np.uint8)

                    if showVideo:
                        print("SHOW VIDEO")
                        frame = self.process({**self.filters}, transparent_img, frame, ".png", self.params)
                    else:
                        frame = self.process({**self.filters}, frame, frame, ".jpg", self.params)

                    yield (b'--frame\r\n'
                           b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')

                    # After all the drawing is finished, we show the frame on the screen
                    # cv2.imshow("preview", frame)

                # at any time, you can press "q" and exit the main loop, therefore exiting the program itself
                # if cv2.waitKey(1) == ord('q'):
                #     break
                else:
                    yield ("error")