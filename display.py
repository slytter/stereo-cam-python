import pygame, sys, os
import time
os.putenv('SDL_FBDEV', '/dev/fb1')

# pygame stuff
pygame.init()
DISPLAYSURF = pygame.display.set_mode((480, 320))
pygame.font.init() # you have to call this at the start, 
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def displayImageOnDisplay(imagePath):
    # set up the window

    img1 = pygame.image.load(os.path.join(imagePath,'0.jpg'))
    # img2 = pygame.image.load(os.path.join(imagePath,'1.jpg'))
    # rn the game loop
    incr = 0
    while True:
        incr+=1
        if(incr%2 == 0):
            DISPLAYSURF.blit(img1,(0,0))
        # else:
        #     DISPLAYSURF.blit(img2,(0,0))
        
        time.sleep(0.1)
        
        for event in pygame.event.get():
                if event.type == pygame.quit:
                            pygame.quit()
                            sys.exit()
        pygame.display.update()
