from RPi import GPIO as GPIO
import time
from threading import Thread

class LedLamp:
    def __init__(self, led=26):
        self.led = led
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT)

    def flikker(self, lengte):
        for i in range(lengte):
            GPIO.output(self.led, GPIO.HIGH)
            time.sleep(.3)
            GPIO.output(self.led, GPIO.LOW)
            time.sleep(.3)

    def flikker_bg(self, lengte):
        background_thread = Thread(target=self.flikker, args=(lengte,))
        background_thread.start()



#LedLamp().flikker(5)
#background_thread = Thread(target=LedLamp().flikker, args=(5,))
#background_thread.start()
#print('test')