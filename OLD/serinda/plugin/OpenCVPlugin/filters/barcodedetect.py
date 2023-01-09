from pyzbar import pyzbar

import cv2
from datetime import datetime

class BarcodeDetect:
    def __init__(self):
        # open the output CSV file for writing and initialize the set of
        # barcodes found thus far
        self.csv = open('barcodes.csv', "w")
        self.found = set()

    def processFilter(self, transparent_img, frame, params):
        # if params['showBarcode']:
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(transparent_img, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(transparent_img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 255), 2)

            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in self.found:
                self.csv.write("{},{}\n".format(datetime.now(), barcodeData))
                self.csv.flush()
                self.found.add(barcodeData)

        return (transparent_img, frame)
