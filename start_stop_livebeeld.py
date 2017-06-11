from sys import executable
from subprocess import Popen
import time


def start():
    global process
    process = Popen([executable, '/home/pi/pistreaming/server.py'])  # start stream
    time.sleep(2)
    print(process)

def stop():
    process.terminate()  # camera kan niet streamen en opnemen tergelijkertijd dus stop stream
    time.sleep(1)