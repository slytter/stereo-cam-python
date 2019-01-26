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
cons.append(Connection('http://slave1.local', ':8080/'))
cons.append(Connection('http://slave3.local', ':8080/'))
cons.append(Connection('http://master.local', ':8080/'))
cons.append(Connection('http://slave2.local', ':8080/'))

connectionThread = threading.Thread(target=connections.updateConnections, args=[cons, 5]) # Update connections in other thread.
connectionThread.start()

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
	class State:
		#optimize by making STATE numbers instead of string
		DEFAULT = 0
		LOADING = 1
		CAPTURE = 2
		SHUT_DOWN = 3
		SHOW_IMAGE = 4

	STATE = State()
	clock = pygame.time.Clock()

	try:
		while 1:
			
			##########################
			# Control block:
			##########################
			if (GPIO.input(butPin) == GPIO.HIGH): # button is released
				program_state = STATE.DEFAULT
			else:
				program_state = STATE.CAPTURE
			if(len(pygameImages) > 0): # if any images in buffer,
				program_state = STATE.SHOW_IMAGE
			elif(GPIO.input(shutDownPin) == GPIO.LOW):
				program_state = STATE.SHUT_DOWN
			
			clock.tick(20)
			# time.sleep(0.01) # sleep for ~ delta 60 fps

			##########################
			# Exacution block:
			##########################
			if(program_state == STATE.DEFAULT):
				for event in pygame.event.get():
					if event.type == USEREVENT+1:
						GUI.defaultScreen(cons)	

			elif(program_state == STATE.CAPTURE):
				print('Shutter pressed')
				connections.enableConnectionCheck(False)
				loadingScreen()
				pygameImages = captureImage()
				connections.enableConnectionCheck(True)

			elif(program_state == STATE.SHOW_IMAGE):
				pygameImages = showLastImage(pygameImages) # show them and remove them

			elif(program_state == STATE.SHUT_DOWN):
				connections.shutDownPis(cons)
	except KeyboardInterrupt:
		GPIO.cleanup() # cleanup all GPIO
		connectionThread.stop()
		pygame.quit()
		return None

	except Exception as e: #Should not close the program on error! Just log message on screen and continue. 
		print('Error in main-loop: ' + str(e))
		GUI.message(str(e))
		time.sleep(2)
		mainLoop(pygameImages)


def loadingScreen():
	GUI.message('please wait', True)

def showLastImage(pygameImages):
	print("showing images.")
	for count in range(0,30): # show for 10 frames
		image = pygameImages[zigzag[count % len(zigzag)]]
		GUI.displayImage(image)
		pygame.time.wait(100)
	return [] # clearing buffer by returning []


def captureImage():
	GPIO.output(ledPin, GPIO.LOW)
	frameBuffers = connectAndDownload(cons)
	GPIO.output(ledPin, GPIO.HIGH)
	if(frameBuffers == False):
		print("Connection error while capturing")
		GUI.message('capture error - could not connect')
		time.sleep(1)
		return []
	pygameImages = []
	for i in range(0, len(frameBuffers)):
		image = pygame.image.load(frameBuffers[i])
		#image = pygame.transform.smoothscale(image, (320, 320)) #Smoothscale will output a better result. But slower.
		image = pygame.transform.scale(image, (320, 320))
		pygameImages.append(image)
	return pygameImages


mainLoop(pygameImages)


