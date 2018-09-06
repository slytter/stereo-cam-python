import GUI
GUI.loadingScreen()
import connections
from connections import Connection
from downloadImages import downloadImages, getLastImagePath
import time
import RPi.GPIO as GPIO
import pygame
from asyncioTest import runIt
from pygame.locals import USEREVENT
#import asyncio
from runcoroutine import runCoroutine
import asyncio 
from asyncio import * 

runIt()
status = False
pingAccuracy = 2
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']


cons = []
cons.append(Connection('http://master.local', ':8080/'))
cons.append(Connection('http://slave1.local', ':8080/'))
cons.append(Connection('http://slave2.local', ':8080/'))
cons.append(Connection('http://slave3.local', ':8080/'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, 1)

GUI.loadingScreen('connected')

runCoroutine(connections.checkClientStatus(cons))

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
ledPin = 27# Broadcom pin 23 (P1 pin 16)
butPin = 17 # Broadcom pin 17 (P1 pin 11)
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GUI.loadingScreen()
GPIO.output(ledPin, GPIO.HIGH)
GUI.loadingScreen()

targetFps = 30
zigzag = [0, 1, 2, 3, 2, 1] # 4 image zig zag
images = []
count = 0
frameShowAmount = 50
framesToShow = frameShowAmount
pygame.time.set_timer(USEREVENT+1, int(1000/targetFps))

try:
	while 1:
		if  (GPIO.input(butPin)): # button is released
			#pwm.ChangeDutyCycle(dc)
			if(len(images) > 0):
				image = images[zigzag[count % 6] % len(images)]
				count+=1
				print(zigzag[count % 6])
				GUI.displayImage(image)
				time.sleep(0.10)
				framesToShow -= 1
				if(framesToShow < 0):
					framesToShow = frameShowAmount
					images = []
			else: #
				for event in pygame.event.get():
					if event.type == USEREVENT+1:
						GUI.defaultScreen(cons)

		else: # button is pressed:
			framesToShow = frameShowAmount
			print('button is pressed...')
			GPIO.output(ledPin, GPIO.LOW)
			frameBuffers = connectAndDownload()
			images = []
			for i in range(0, len(frameBuffers)):
				image = pygame.image.load(frameBuffers[i]).convert_alpha()
				image = pygame.transform.smoothscale(image, (320, 320))
				images.append(image)
				
			GPIO.output(ledPin, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(ledPin, GPIO.LOW)
			time.sleep(0.075)
			GPIO.output(ledPin, GPIO.HIGH)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup() # cleanup all GPIO
