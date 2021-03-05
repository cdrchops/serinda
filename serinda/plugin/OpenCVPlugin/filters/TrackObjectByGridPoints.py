# from Mastering-OpenCV-4-with-Python Chapter 11
# removed mouse selection
# adding voice selection
# track object at 50 and 75 by 150 pixels (x = 50, y = 50, 150 pixel square)

import dlib
import cv2

class TrackObjectByGridPoints:
    # First step is to initialize the correlation tracker.
    tracker = dlib.correlation_tracker()
    params = {}

    def __init__(self, params):
        self.params = params

    def processFilter(self, transparent_img, frame, params):
        # if params['trackObjectByGrid']:

        # self.params['gridX'] = 150
        # self.params['gridY'] = 150
        # self.params['sizeOfArea'] = 50

        # if gridX exists then we want to use those values
        # gridX, gridY, and sizeOfArea should be deleted from the params after the first set - however, the command
        # was changed in camera so it's empty and that seems to have fixed the issue
        # TODO: speed test the changes against all of these filters in static methods inside of camera
        #         or even static cameras defined and hitting all of these filters
        #         also test 1 camera vs 3-4
        if 'gridX' in self.params.keys():
            self.points = [(int(self.params['gridX']), int(self.params['gridY'])),
                           (int(self.params['gridX']) + int(self.params['sizeOfArea']), int(self.params['gridY']) + int(self.params['sizeOfArea']))]

        # We set and draw the rectangle where the object will be tracked if it has the two points:
        if len(self.points) == 2:
            points = self.points
            cv2.rectangle(frame, points[0], points[1], (0, 0, 255), 2)
            cv2.rectangle(transparent_img, points[0], points[1], (0, 0, 255, 255), 2)
            dlib_rectangle = dlib.rectangle(points[0][0], points[0][1], points[1][0], points[1][1])
            self.tracker.start_track(frame, dlib_rectangle)
            self.points = []

        # Update tracking
        self.tracker.update(frame)
        # Get the position of the tracked object:
        pos = self.tracker.get_position()
        # Draw the position:
        cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())), (0, 255, 0), 2)
        cv2.rectangle(transparent_img, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())), (0, 255, 0, 255), 2)

        return (transparent_img, frame)
