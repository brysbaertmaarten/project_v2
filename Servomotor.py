import RPi.GPIO as GPIO
import time


class ServoMotor:

    def __init__(self, servo=21, position=50):
        self.__servo = servo
        self.__position = position

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo, GPIO.OUT)

    def relative_rotate(self, percentage):
        self.__position += percentage
        if self.__position > 100 or self.__position < 0:
            self.__position -= percentage
        self.absolute_rotate(self.__position)

    def get_position(self):
        return self.__position

    def center_rotate(self):
        ServoMotor.__position = 50
        self.absolute_rotate(50)

    def left_rotate(self):
        ServoMotor.__position = 100
        self.absolute_rotate(100)

    def right_rotate(self):
        ServoMotor.__position = 0
        self.absolute_rotate(0)

    def step_left(self):
        self.relative_rotate(5)

    def step_right(self):
        self.relative_rotate(-5)

    def absolute_rotate(self, position):
        #pulse in totaal: 20ms, pulse high: tussen .5 ms en 2.4 ms
        ServoMotor.__position = position
        omgerekende_waarde = ((int(position) / 100) * 0.0019) + 0.0005
        if (omgerekende_waarde >= 0.0005) and (omgerekende_waarde <= 0.00241):
            for i in range(20):
                GPIO.output(self.__servo, GPIO.HIGH)
                time.sleep(omgerekende_waarde)
                GPIO.output(self.__servo, GPIO.LOW)
                time.sleep(0.020 - omgerekende_waarde)

