from RPi import GPIO as GPIO
import time
import camera
from Led import LedLamp
from Buzzer import Buzzer
from DbClass import DbClass
import datetime
import start_stop_livebeeld

class MotionSensor:
    def __init__(self, motion_sensor = 21):
        self.motion_sensor = motion_sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motion_sensor, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.motion_sensor, GPIO.RISING, self.detected, 10000)
        print('inint')

    def detected(self, pin):
        settings = DbClass().getDataFromDatabase('settings')[0]
        print("motion detected")

        if settings[1]:
            start_stop_livebeeld.stop()
            dateTime = datetime.datetime.now()
            DbClass().insertMedia(1, 'naamloos', 1, dateTime)
            data = DbClass().getDataFromDatabaseMetVoorwaarde('media', 'date', dateTime)
            identifier = data[0][0]
            camera.PiCam().start_record(str(identifier))
            print('start recording')

            if settings[4]:
                print('led')
                LedLamp().flikker(5)

            if settings[3]:
                print('alarm')
                Buzzer().alarm(5)

            if settings[5]:
                print('email send')

