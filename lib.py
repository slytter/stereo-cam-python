import RPi.GPIO as GPIO
import time

def waitForPullUp(pin):
    while(GPIO.input(pin) == GPIO.LOW):
        time.sleep(0.05) # sleep for ~ delta 60 fps
        
