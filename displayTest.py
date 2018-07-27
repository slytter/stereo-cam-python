import pygame, sys, os
from pygame.locals import *
import time
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((480, 320))
pygame.mouse.set_visible(False)
font = pygame.font.Font("Futura.ttc", 20)
text = font.render("loading", True, (255, 255, 255))

img1 = pygame.image.load(os.path.join('slyt_logo.png')).convert_alpha()
w,h = img1.get_size()
img1 = pygame.transform.smoothscale(img1, (int(float(w)/2.0), int(float(h)/2.0)))
w,h = img1.get_size()

#pygame.image.save(DISPLAYSURF, 'test.png')
#background = pygame.Surface(window)
# rn the game loop
incr = 0
def modColor(val):
	return val % 255

#pygame.display.set_gamma_ramp()

clock = pygame.time.Clock()
def timerFunc():
	incr
	clock.tick()
	print(clock.get_fps())
	#baseColor = modColor(incr)
	DISPLAYSURF.fill(pygame.Color(0,0,0))
	#pygame.draw.rect(DISPLAYSURF, pygame.Color(100,100,100), (0,0,480, 320))
	pygame.display.update()


pygame.init()
pygame.time.set_timer(USEREVENT+1, 50)
while 1:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			timerFunc() #calling the function wheever we get timer event.
			
		if event.type == QUIT:
			break


deltaFrameTime = 0
while True:
	incr+=1
	#DISPLAYSURF.fill(pygame.Color(modColor(incr + 40), modColor(incr), modColor(incr+200)))
	baseColor = modColor(incr)
	pygame.draw.rect(DISPLAYSURF, pygame.Color(baseColor, baseColor, baseColor), (0,0,480, 320))
	#DISPLAYSURF.blit(img1,(480/2 - w/2, 320/2 - h/2), (0, 0, 480, 320))
	#DISPLAYSURF.blit(text, (480/2 - text.get_width() // 2, 320/2 - text.get_height() // 2 + 50))
	#time.sleep(0.005)
	print(incr)
#	for col in range(0,255):
#		pygame.draw.line(DISPLAYSURF, pygame.Color(col,col,col), (col, 0), (col,50))
#		pygame.draw.line(DISPLAYSURF, pygame.Color(col,0,0), (col, 50), (col,100))
#		pygame.draw.line(DISPLAYSURF, pygame.Color(0,col,0), (col, 100), (col,150))
#		pygame.draw.line(DISPLAYSURF, pygame.Color(0,0,col), (col, 150), (col,200))
	pygame.display.update()
		

		



'''	for event in pygame.event.get():
			if event.type == QUIT:
						pygame.quit()
						sys.exit()'''

