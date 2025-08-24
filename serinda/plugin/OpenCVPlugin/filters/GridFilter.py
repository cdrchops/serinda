import cv2

class GridFilter:
    line_color = (0, 255, 0)
    thickness = 1
    type_ = cv2.LINE_AA
    pxstep = 50

    # https://stackoverflow.com/questions/44816682/drawing-grid-lines-across-the-image-uisng-opencv-python
    def processFilter(self, transparent_img, frame, params):
        if params['showGrid']:
            '''(ndarray, 3-tuple, int, int) -> void
            draw gridlines on img
            line_color:
                BGR representation of colour
            thickness:
                line thickness
            type:
                8, 4 or cv2.LINE_AA
            pxstep:
                grid line frequency in pixels
            '''
            x = self.pxstep
            y = self.pxstep
            charx = 1
            chary = 1
            while x < frame.shape[1]:
                cv2.line(frame, (x, 0), (x, frame.shape[0]), color=self.line_color, lineType=self.type_, thickness=self.thickness)
                # for lowercase change chr(ord('@') + charx) to chr(ord('`') + charx)
                # https://stackoverflow.com/questions/23199733/convert-numbers-into-corresponding-letter-using-python/46399948
                cv2.putText(frame, chr(ord('@') + charx), (x - 30, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                x += self.pxstep
                charx += 1

            cv2.putText(frame, chr(ord('@') + charx), (x - 30, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            while y < frame.shape[0]:
                cv2.line(frame, (0, y), (frame.shape[1], y), color=self.line_color, lineType=self.type_, thickness=self.thickness)
                cv2.putText(frame, str(chary), (10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                y += self.pxstep
                chary += 1

            cv2.putText(frame, str(chary), (10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return (transparent_img, frame)
