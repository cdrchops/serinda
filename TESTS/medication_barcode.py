# https://open.fda.gov/apis/drug/ndc/
# https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory

import cv2
from pyzbar import pyzbar
from pylibdmtx.pylibdmtx import decode

class MedicationBarcode:

    def __init__(self, basePath, image):
        self.basePath = basePath
        self.imagePath = self.basePath + image
        self.tmpImage = cv2.imread(self.imagePath, 0)
        self.image = cv2.resize(self.tmpImage, (960, 540))
        self.decodedObjects = pyzbar.decode(self.image)

    # b'0100304870201018211110430744451726022810427141
    # GTIN: 01 00304870201018
    # SN: 21 111043074445
    # EXP: 17 260228
    # LOT: 10 427141
    def decode_data_matrix(self, tmpImage):
        return decode(tmpImage)
        # print(decode(tmpImage))

    # data bar code
    # 0100301439875017
    # 01003
    # 0143-9875
    # 017
    def lookup_data_barcode(self, obj):
        data = obj.data.decode('utf-8')
        return data[5:9] + '-' + data[9:13]

    def run(self):
        if self.decodedObjects == []:
            # print('No barcode detected')
            decoded = self.decode_data_matrix(self.tmpImage)
            return ["DATAMATRIX", decoded]

        # Print results
        for obj in self.decodedObjects:
            # print('Type:', obj.type)
            # print('Data:', obj.data.decode('utf-8'))
            # if obj.type == 'DATABAR':
            return [obj.type, self.lookup_data_barcode(obj)]