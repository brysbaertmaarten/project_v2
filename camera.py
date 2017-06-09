from picamera import PiCamera
import time
import os


class PiCam:
    def __init__(self):
        self.camera = PiCamera()

    def start_record(self, identifier):
        self.camera.start_recording("/home/pi/Documents/python/static/media/" + identifier + "_vid.h264")

    def stop_record(self):
        self.camera.stop_recording()

    def set_to_mp4(self):
        os.system('avconv -r 30 -i /home/pi/Documents/python/static/media/testje.h264 -vcodec copy /home/pi/Documents/python/static/media/testje.mp4')

