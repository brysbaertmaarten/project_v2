from RPi import GPIO as GPIO
import time
from threading import Thread


class Buzzer:
    def __init__(self, buzzer=13):
        self.buzzer = buzzer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer, GPIO.OUT)

    def alarm(self, lengte):
        for i in range(lengte):
            GPIO.output(self.buzzer, GPIO.HIGH)
            time.sleep(.3)
            GPIO.output(self.buzzer, GPIO.LOW)
            time.sleep(.3)

    def alarm_bg(self, lengte):
        background_thread = Thread(target=self.alarm, args=(lengte,))
        background_thread.start()


#LedLamp().flikker(5)