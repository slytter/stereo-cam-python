import GUI
GUI.loadingScreen()
import connections
from connections import Connection
from downloadImages import connectAndDownload
import time
import RPi.GPIO as GPIO
import pygame
from pygame.locals import USEREVENT
import threading
import sequenceGen

status = False
pingAccuracy = 2

cons = []
cons.append(Connection('http://master.local', ':8080/'))
cons.append(Connection('http://slave1.local', ':8080/'))
cons.append(Connection('http://slave2.local', ':8080/'))
cons.append(Connection('http://slave3.local', ':8080/'))

threading.Thread(target=connections.updateConnections, args=[cons, 5]).start() # Update connections in other thread.

# Pin Definitons:
ledPin = 27
butPin = 17 # Broadcom pin 17 (P1 pin 11)
shutDownPin = 3

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(shutDownPin, GPIO.IN)
GPIO.output(ledPin, GPIO.HIGH)
GPIO.setwarnings(False)

GUI.loadingScreen()

targetFps = 30
zigzag = sequenceGen.zigZag(len(cons))
pygameImages = []
pygame.time.set_timer(USEREVENT+1, int(1000/targetFps))


def mainLoop(pygameImages):
	try:
		while 1:
			if (GPIO.input(butPin) == GPIO.HIGH): # button is released
				time.sleep(0.016) # sleep for ~ delta 60 fps
				for event in pygame.event.get():
					if event.type == USEREVENT+1:
						GUI.defaultScreen(cons)	
				
				if(GPIO.input(shutDownPin) == GPIO.LOW):
					connections.shutDownPis(cons)
				
				if(len(pygameImages) > 0): # if any images in buffer,
					pygameImages = showLastImage(pygameImages) # show them and remove them
					
			else: # button is pressed:
				print('Shutter pressed')
				connections.enableConnectionCheck(False)
				pygameImages = captureImage()
				connections.enableConnectionCheck(True)

	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
		GPIO.cleanup() # cleanup all GPIO


def showLastImage(pygameImages):
	for count in range(0,30): # show for 10 frames
		image = pygameImages[zigzag[count % len(zigzag)]]
		GUI.displayImage(image)
		pygame.time.wait(100)
	return [] # clearing buffer by returning []


def captureImage():
	GPIO.output(ledPin, GPIO.LOW)
	frameBuffers = connectAndDownload(cons)
	if(frameBuffers == False):
		print("Connection error while capturing")
		GUI.message('capture error - could not connect')
		time.sleep(1)
		return []
	pygameImages = []
	for i in range(0, len(frameBuffers)):
		image = pygame.image.load(frameBuffers[i])
		image = pygame.transform.smoothscale(image, (320, 320))
		pygameImages.append(image)
	return pygameImages


mainLoop(pygameImages)


