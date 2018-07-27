import pygame, sys, os
import pygame
import time
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((480, 320))

img1 = pygame.image.load(os.path.join('test.png'))
img2 = pygame.image.load(os.path.join('mor.png'))
DISPLAYSURF.blit(img1,(0,0), (0, 0, 480, 320))
#pygame.image.save(DISPLAYSURF, 'test.png')
#background = pygame.Surface(window)
# rn the game loop
incr = 0
while True:
	incr+=7
	pygame.transform.scale(DISPLAYSURF, (480,320))
	DISPLAYSURF.blit(img1,(0,0), (0, 0, 480, 320))
	
	time.sleep(1/30)
	negativeIncr = 320 - (incr % 320)
	pygame.draw.line(DISPLAYSURF, pygame.Color(255, 255, 255, 255), (480, negativeIncr), (0, incr % 320))
	pygame.draw.line(DISPLAYSURF, pygame.Color(255, 0, 0, 255), (480, negativeIncr), (60, incr % 320 + 50))
	pygame.draw.line(DISPLAYSURF, pygame.Color(0, 0, 255, 255), (480, negativeIncr), (0, incr % 320 + 100))
	pygame.draw.line(DISPLAYSURF, pygame.Color(0, 255, 0, 255), (480, negativeIncr), (60, incr % 320 + 150))
	
	for event in pygame.event.get():
			if event.type == QUIT:
						pygame.quit()
						sys.exit()
	pygame.display.update()

