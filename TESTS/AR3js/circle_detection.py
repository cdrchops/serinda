import cv2
import time
import math
import numpy as np

capture = cv2.VideoCapture(0)
print(capture.get(cv2.CAP_PROP_FPS))

t = 100
w = 640.0

last = 0
while True:
    ret, image = capture.read()
    
    img_height, img_width, depth = image.shape
    scale = w / img_width
    h = img_height * scale
    image = cv2.resize(image, (0,0), fx=scale, fy=scale)

    # Apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(grey, 15)

    # Compose 2x2 grid with all previews
    grid = np.zeros([2*h, 2*w, 3], np.uint8)
    grid[0:h, 0:w] = image

    # We need to convert each of them to RGB from grescaled 8 bit format
    grid[h:2*h, 0:w] = np.dstack([cv2.Canny(grey, t / 2, t)] * 3)
    grid[0:h, w:2*w] = np.dstack([blured] * 3)
    grid[h:2*h, w:2*w] = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)

    cv2.imshow('Image previews', grid)

    sc = 1
    md = 30
    at = 40
    circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, sc, md, t, at)

    if circles is not None:
        # We care only about the first circle found.
        circle = circles[0][0]
        x, y, radius = int(circle[0]), int(circle[1]), int(circle[2])
        print(x, y, radius)

        # Highlight the circle
        cv2.circle(image, (x, y), radius, (0, 0, 255), 1)
        # Draw dot in the center
        cv2.circle(image, (x, y), 1, (0, 0, 255), 1)

    cv2.imshow('Image with detected circle', image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break