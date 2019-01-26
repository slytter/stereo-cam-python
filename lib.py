import RPi.GPIO as GPIO
import time

def waitForPullUp(pin):
	while(GPIO.input(pin) == GPIO.LOW):
		time.sleep(0.05) # sleep for ~ delta 50ms
	
def waitXThenPullUp(pin, X): # not implemented
	timestamp = time.time()
	while(GPIO.input(pin) == GPIO.LOW and time.time() > timestamp + X):
		time.sleep(0.05) # sleep for ~ delta delta 16ms
	
