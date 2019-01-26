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
import lib
import gallery
status = False
pingAccuracy = 2

cons = []
cons.append(Connection('http://slave1.local', ':8080/'))
# cons.append(Connection('http://master.local', ':8080/'))
cons.append(Connection('http://master2.local', ':8080/'))
# cons.append(Connection('http://slave2.local', ':8080/'))
# cons.append(Connection('http://slave3.local', ':8080/'))

threading.Thread(target=connections.updateConnections, args=[cons, 5]).start() # Update connections in other thread.

# Pin Definitons:
ledPin = 21
butPin = 20 # Broadcom pin 17 (P1 pin 11)
shutDownPin = 3
mainButton = 5
scrollRight = 13
scrollLeft = 6
# Pin Setup:
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(scrollRight, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(scrollLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(mainButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(shutDownPin, GPIO.IN)

GPIO.output(ledPin, GPIO.HIGH)
GUI.loadingScreen()

targetFps = 30
zigzag = sequenceGen.zigZag(len(cons))
pygameImages = []
pygame.time.set_timer(USEREVENT+1, int(1000/targetFps))


class State:
	DEFAULT = 0
	LOADING = 1
	CAPTURE = 2
	SHUT_DOWN = 3
	SHOW_IMAGE = 4
	GALLERY = 5

STATE = State()
program_state = 0


def mainLoop(pygameImages):
	try:
		while 1:
			##########################
			# Toggle Block:
			##########################
			# elif(GPIO.input(scrollRight) == GPIO.LOW):
			# 	print("test")
			##########################
			# Control block:
			##########################
			global program_state
			if (GPIO.input(butPin) == GPIO.LOW): # Shutter button is pressed
				program_state = STATE.CAPTURE
				print('test1')
			elif(len(pygameImages) > 0): # if any images in buffer,
				program_state = STATE.SHOW_IMAGE
				print('test2')
			elif(GPIO.input(shutDownPin) == GPIO.LOW): 
				program_state = STATE.SHUT_DOWN
			elif(GPIO.input(mainButton) == GPIO.LOW): #If gallery button is pressed
				print(program_state)
				if(program_state == STATE.GALLERY): # if we are 
					program_state = STATE.DEFAULT
				else:
					program_state = STATE.GALLERY
					gallery.setup()
				lib.waitForPullUp(mainButton)

			elif(program_state != STATE.GALLERY):
				program_state = STATE.DEFAULT
			time.sleep(0.01) # sleep for ~ delta 60 fps

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
			elif(program_state == STATE.GALLERY):
				gallery.draw()
				if(GPIO.input(scrollLeft) == GPIO.LOW):
					GUI.gallery(-1)
					lib.waitXThenPullUp(scrollLeft, 50)
				elif(GPIO.input(scrollRight) == GPIO.LOW):
					GUI.gallery(1)
					lib.waitXThenPullUp(scrollRight, 50)
				else:
					GUI.gallery()

	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
		GPIO.cleanup() # cleanup all GPIO
		pygame.quit()


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
	try:
		frameBuffers, thumpImageNames = connectAndDownload(cons)
	except TypeError as e:
		GUI.message("One or more slave(s) returned 500")
		time.sleep(2)
		return []
	except Exception as e:
		GUI.message(str(e))
		time.sleep(2)
		return []

	GPIO.output(ledPin, GPIO.HIGH)
	if(frameBuffers == False):
		print("Connection error while capturing")
		GUI.message('capture error - could not connect')
		time.sleep(1.5)
		return []
	pygameImages = []
	for i in range(0, len(frameBuffers)):
		image = pygame.image.load(frameBuffers[i])
		#image = pygame.transform.smoothscale(image, (320, 320)) #Smoothscale will output a better result. But slower.
		image = pygame.transform.scale(image, (320, 320))
		pygame.image.save(image, thumpImageNames[i])
		pygameImages.append(image)
	return pygameImages


mainLoop(pygameImages)
