import connections
from connections import Connection
from downloadImages import downloadImages 
from downloadImages import getLastImagePath
import time, os
import RPi.GPIO as GPIO
import pygame
from pygame.locals import USEREVENT
import math
import asyncio
from runcoroutine import runCoroutine

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
DISPLAYSURF = pygame.display.set_mode((480, 320))
pygame.mouse.set_visible(False)
font = pygame.font.Font("Futura.ttc", 20)
small_font = pygame.font.Font("Futura.ttc", 15)
text = font.render("loading", True, (255, 255, 255))
cons = []


img1 = pygame.image.load(os.path.join('slyt_logo.png')).convert_alpha()
w,h = img1.get_size()
img1 = pygame.transform.smoothscale(img1, (int(float(w)/2.0), int(float(h)/2.0)))
w,h = img1.get_size()

incr = 0
def modColor(val):
	return val % 255

def loadingScreen():
	global incr
	incr+=50
	DISPLAYSURF.fill(pygame.Color(modColor(incr + 40), modColor(incr), modColor(incr+200)))
	pygame.draw.rect(DISPLAYSURF, pygame.Color(100,0,0), (0,0,480, 320))
	DISPLAYSURF.blit(img1,(480/2 - w/2, 320/2 - h/2), (0, 0, 480, 320))
	DISPLAYSURF.blit(text, (480/2 - text.get_width() // 2, 320/2 - text.get_height() // 2 + 50))
	time.sleep(0.005)
	pygame.display.update()

loadingScreen()


frontScreenText1 = font.render("shutter ready", True, (255, 255, 255))
frontScreenText2 = small_font.render("release shutter when all shutter-indicators are synced", True, (255, 255, 255))

checkConnectionEveryXFrame = 100
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
incrD = 0.0
clock = pygame.time.Clock()
def defaultScreen():
	clock.tick()
	# print(clock.get_fps())

	ok = True
	if(int(incrD) % checkConnectionEveryXFrame == 0):
		print('before corou')
		runCoroutine(connections.checkClientStatus(cons)) # can this be done in a coroutine?
		print('after corou')
	for i in range(0,len(cons)):
		ind_col = white
		if(cons[i].ping > 30):
			ind_col = pygame.Color(255,50,50)
		pygame.draw.ellipse(DISPLAYSURF, ind_col, (10 + 30 * i, 10, 20, 20))
		if (cons[i].status == False or cons[i].serverUp == False):
			ok = False
			pygame.draw.ellipse(DISPLAYSURF, pygame.Color(0,0,0), (12 + 30 * i, 12, 16, 16))
	if(ok == True):
		okmsg = small_font.render("ok", True, (255, 255, 255))
	else:
		okmsg = small_font.render("connection error", True, (255, 255, 255))

	if(ok == True):
		global incrD 
		incrD += 1.0
		DISPLAYSURF.fill(black)
		DISPLAYSURF.blit(frontScreenText1, (480/2 - frontScreenText1.get_width() // 2, 400/2 - frontScreenText1.get_height() // 2))
		#time.sleep(0.005)
		col = int(abs(math.sin(incrD/100.0) * 100))
		movement = int(abs(math.sin(incrD/50.0) * 50))
		pygame.draw.line(DISPLAYSURF, white, (480/2, 320/2 - 120 + movement), (480/2, 320/2 - 80 + movement))
		pygame.draw.line(DISPLAYSURF, white, (480/2, 320/2 - 80 + movement), (480/2 + 10, 320/2 - 90 + movement))
		pygame.draw.line(DISPLAYSURF, white, (480/2, 320/2 - 80 + movement), (480/2 - 10, 320/2 - 90 + movement))
		pygame.draw.ellipse(DISPLAYSURF, pygame.Color(col,col,col, col), (480/2 - 35, 400/2 - 64, 70, 23))
		pygame.draw.ellipse(DISPLAYSURF, black, (480/2 - 30, 400/2 - 65, 60, 20))
	else: 
		DISPLAYSURF.blit(frontScreenText2, (480/2 - frontScreenText2.get_width() // 2, 400/2 - frontScreenText2.get_height() // 2))

	DISPLAYSURF.blit(okmsg, ((len(cons) * 30) + 10, 9))

	pygame.display.update()

status = False
pingAccuracy = 4
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']


cons.append(Connection('http://master.local', ':8080/'))
cons.append(Connection('http://slave1.local', ':8080/'))
cons.append(Connection('http://slave2.local', ':8080/'))
cons.append(Connection('http://slave3.local', ':8080/'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, pingAccuracy)
loadingScreen()

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
loadingScreen()

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.HIGH)
GPIO.output(shutterPin, GPIO.LOW)
pwm.start(dc)
loadingScreen()

zigzag = [0, 1, 2, 3, 2, 1] # 4 image zig zag
images = []
count = 0
frameShowAmount = 20
framesToShow = frameShowAmount
pygame.time.set_timer(USEREVENT+1, 40)

try:
	while 1:
		if  (GPIO.input(butPin)): # button is released
			#pwm.ChangeDutyCycle(dc)
			if(len(images) > 0):
				image = images[zigzag[count % 6] % len(images)]
				count+=1
				print(zigzag[count % 6])
				DISPLAYSURF.set_colorkey(image.get_colorkey())
				DISPLAYSURF.blit(image,(80,0), (0, 0, 480, 320))
				pygame.display.update()
				time.sleep(0.10)
				framesToShow -= 1
				if(framesToShow < 0):
					framesToShow = frameShowAmount
					images = []
			else:
				for event in pygame.event.get():
					if event.type == USEREVENT+1:
						defaultScreen()

		else: # button is pressed:
			framesToShow = frameShowAmount
			print('button is pressed...')
			GPIO.output(ledPin, GPIO.LOW)
			#pwm.ChangeDutyCycle(100-dc)
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
	pwm.stop() # stop PWM
	GPIO.cleanup() # cleanup all GPIO




