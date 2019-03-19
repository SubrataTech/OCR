import cv2
import sys
import logging as log
import datetime as dt
from time import sleep

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing  from a webcam,
        # comment the line below out and use a video file instead.
        self.video = cv2.VideoCapture(0)

        # self.video = cv2.VideoCapture('video.mp4')   # to use video

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            a = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # print a
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
