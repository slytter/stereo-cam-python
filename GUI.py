import os, pygame, time, math
from runcoroutine import runCoroutine
import connections
print('0')

os.putenv('SDL_FBDEV', '/dev/fb0')
print('1')
pygame.init()
print('2')

DISPLAYSURF = pygame.display.set_mode((480, 320))
print('3')

pygame.mouse.set_visible(False)
font = pygame.font.Font("Futura.ttc", 20)
small_font = pygame.font.Font("Futura.ttc", 15)
text = font.render("loading", True, (255, 255, 255))


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

checkConnectionEveryXFrame = 100
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
incrD = 0.0
clock = pygame.time.Clock()
def defaultScreen(cons):
	clock.tick()
	# print(clock.get_fps())
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

	DISPLAYSURF.blit(okmsg, ((len(cons) * 30) + 10, 9))
	pygame.display.update()

def displayImage(image):
    DISPLAYSURF.set_colorkey(image.get_colorkey())
    DISPLAYSURF.blit(image,(80,0), (0, 0, 480, 320))
    pygame.display.update()

