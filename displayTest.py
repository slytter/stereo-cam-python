import pygame, sys, os
import pygame
import time
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((480, 320))

img1 = pygame.image.load(os.path.join('0.jpg'))
img2 = pygame.image.load(os.path.join('1.jpg'))
# rn the game loop
incr = 0
while True:
	incr+=1
	if(incr%2 == 0):
		DISPLAYSURF.blit(img1,(0,0))
	else:
		DISPLAYSURF.blit(img2,(0,0))
	
	time.sleep(0.1)
	pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, incr % 320))
	
	for event in pygame.event.get():
			if event.type == QUIT:
						pygame.quit()
						sys.exit()
	pygame.display.update()

