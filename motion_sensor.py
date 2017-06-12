from RPi import GPIO as GPIO
import time
import camera
from Led import LedLamp
from Buzzer import Buzzer
from DbClass import DbClass
import datetime

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
            print('start recording')

            if settings[4]:
                print('led')
                LedLamp().flikker_bg(5)

            if settings[3]:
                print('alarm')
                Buzzer().alarm_bg(5)

            if settings[5]:
                print('email send')

