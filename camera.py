from picamera import PiCamera
import time
import os


class PiCam:
    def __init__(self):
        self.camera = PiCamera()

    def start_record(self, identifier):
        pad = "/home/pi/Documents/python/project_v2/static/media/" + identifier + "_vid."
        self.camera.start_recording(pad + 'h264')
        time.sleep(5)
        self.camera.stop_recording()
        self.camera.close()
        self.set_to_mp4(pad)

    def set_to_mp4(self, pad):
        os.system('avconv -r 30 -i ' + pad + 'h264 -vcodec copy ' + pad + 'mp4')

    def capture(self, identifier):
        pad = "/home/pi/Documents/python/project_v2/static/media/" + identifier + "_pic."
        self.camera.capture(pad + 'jpg')
        self.camera.close()

