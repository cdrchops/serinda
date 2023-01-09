from datetime import datetime
import cv2

class TimestampDisplayFilter:
    def processFilter(self, transparent_img, frame, params):
        # if intent == "timestamp":
        #     self.timestamp = not self.timestamp

        # if params['showTimestamp']:
        # grab the current timestamp and draw it on the frame
        timestampDatetime = datetime.now()
        cv2.putText(frame,
                    timestampDatetime.strftime("%A %d %B %Y %I:%M:%S%p"),
                    (50, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    (0, 0, 255),
                    1)

        cv2.putText(transparent_img,
                    timestampDatetime.strftime("%A %d %B %Y %I:%M:%S%p"),
                    (50, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    (0, 0, 255, 255),
                    1)

        return (transparent_img, frame)
