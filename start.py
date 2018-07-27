import connections
from connections import Connection
from downloadImages import downloadImages 
from downloadImages import getLastImagePath
import time, os
import RPi.GPIO as GPIO
import pygame

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

DISPLAYSURF = pygame.display.set_mode((480, 320))


status = False
pingAccuracy = 4
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']

cons = []

#cons.append(Connection('http://master.local', ':8080/capture'))
cons.append(Connection('http://slave1.local', ':8080/capture'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, pingAccuracy)



def connectAndDownload():
	started = time.time()
	print('Starting requests')
	frameBuffers = downloadImages(cons, 10)
	if(len(frameBuffers) != 0):
		print(len(frameBuffers))
		print('Succesfully downloaded and compiled. It took: ' + str(time.time()-started) + ' secs')
		return frameBuffers
	else:
		print('Download error. Re-pinging slaves')
		global status
		status = connections.pingConnections(cons, pingAccuracy)
		return False



# Pin Definitons:
pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
ledPin = 27# Broadcom pin 23 (P1 pin 16)
butPin = 17 # Broadcom pin 17 (P1 pin 11)
shutterPin = 4

dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
GPIO.setup(shutterPin, GPIO.OUT) # LED pin set as output
GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.HIGH)
GPIO.output(shutterPin, GPIO.LOW)
pwm.start(dc)


print('eskitit')
print("Here we go! Press CTRL+C to exit")
try:
	while 1:
		if  (GPIO.input(butPin)): # button is released
			pwm.ChangeDutyCycle(dc)
#			GPIO.output(ledPin, GPIO.HIGH)
		else: # button is pressed:
			print('button is pressed...')
			GPIO.output(ledPin, GPIO.LOW)
			pwm.ChangeDutyCycle(100-dc)
			frameBuffers = connectAndDownload()
			#pygame.surfarray.make_surface(frameBuffers[0])
			img1 = pygame.image.load(frameBuffers[0])
			DISPLAYSURF.blit(img1,(0,0), (0, 0, 480, 320))
			pygame.display.update()
			GPIO.output(ledPin, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(ledPin, GPIO.LOW)
			time.sleep(0.075)
			GPIO.output(ledPin, GPIO.HIGH)
			#os.system("sudo fbi -noverbose -T 1 -a -d /dev/fb1 " + getLastImagePath())
			#print("sudo fbi -noverbose -T 1 -a -d /dev/fb1 " + getLastImagePath() +"/1.jpg")
#			display.displayImageOnDisplay(getLastImagePath())
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	pwm.stop() # stop PWM
	GPIO.cleanup() # cleanup all GPIO
