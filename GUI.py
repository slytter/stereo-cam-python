import os, pygame, time, math
# from runcoroutine import runCoroutine

os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
DISPLAYSURF = pygame.display.set_mode((480, 320))

### TEXT RENDERS ###
pygame.mouse.set_visible(False)
font = pygame.font.Font("Futura.ttc", 20)
small_font = pygame.font.Font("Futura.ttc", 15)
frontScreenText1 = font.render("shutter ready", True, (255, 255, 255))


img1 = pygame.image.load(os.path.join('slyt_logo.png')).convert_alpha()
w,h = img1.get_size()
img1 = pygame.transform.smoothscale(img1, (int(float(w)/2.0), int(float(h)/2.0)))
w,h = img1.get_size()

incr = 0
checkConnectionEveryXFrame = 100
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
red = pygame.Color(255,50,50)
incrD = 0.0
clock = pygame.time.Clock()
half = [480/2, 320/2]

def modColor(val):
	return val % 255

def loadingScreen(msg = 'loading', cons = None, anyConnectionDown = 0):

	if(anyConnectionDown > 0):
		GUI.loadingScreen(str(anyConnectionDown) + ' connection' + ('' if(anyConnectionDown == 1) else 's') + ' down')
		GUI.renderConnectionDots(cons)
		GUI.pygame.display.update()

	global incr
	incr+=15
	text = font.render(msg, True, (255, 255, 255))
	DISPLAYSURF.fill(pygame.Color(modColor(incr + 40), modColor(incr), modColor(incr+200)))
	# pygame.draw.rect(DISPLAYSURF, pygame.Color(100,0,0), (0,0,480, 320))
	DISPLAYSURF.blit(img1,(480/2 - w/2, 320/2 - h/2), (0, 0, 480, 320))
	DISPLAYSURF.blit(text, (480/2 - text.get_width() // 2, 320/2 - text.get_height() // 2 + 50))
	# pygame.draw.rect(DISPLAYSURF, pygame.Color(255,255,255), (0, 0, 480, 320))
	time.sleep(0.005)
	pygame.display.update()

def defaultScreen(cons):
	DISPLAYSURF.fill(black)
	clock.tick()
	global incrD 
	incrD += 1.0
	# if(int(incrD) % checkConnectionEveryXFrame == 0):
	# 	runCoroutine(connections.checkClientStatus(cons)) # can this be done in a coroutine?
	
	ok = renderConnectionDots(cons)

	if(ok == True):
		okmsg = small_font.render("ok", True, (255, 255, 255))
	else:
		okmsg = small_font.render("connection error", True, (255, 255, 255))

	drawAnimation(ok, incr)
	DISPLAYSURF.blit(okmsg, ((len(cons) * 30) + 10, 9))
	pygame.display.update()



def displayImage(image):
	DISPLAYSURF.fill(white)
	#   DISPLAYSURF.set_colorkey(image.get_colorkey())
	DISPLAYSURF.blit(image,(80,0), (0, 0, 480, 320))
	pygame.display.update()


def drawAnimation(ready, incr):
	if(ready):
		movement = int((1 + math.sin(incrD/15.0))/2*50)
		DISPLAYSURF.blit(frontScreenText1, (480/2 - frontScreenText1.get_width() // 2, 400/2 - frontScreenText1.get_height() // 2))
		pygame.draw.line(DISPLAYSURF, white, (half[0], half[1] - 120 + movement), (half[0], half[1] - 80 + movement))
		pygame.draw.line(DISPLAYSURF, white, (half[0], half[1] - 80 + movement), (half[0] + 10, half[1] - 90 + movement))
		pygame.draw.line(DISPLAYSURF, white, (half[0], half[1] - 80 + movement), (half[0] - 10, half[1] - 90 + movement))
	else:
		pygame.draw.line(DISPLAYSURF, red, (half[0] - 10, half[1] - 45), (half[0] + 10, half[1] - 65))
		pygame.draw.line(DISPLAYSURF, red, (half[0] + 10, half[1] - 45), (half[0] - 10, half[1] - 65))

	col = int((1 + math.sin(incrD/15.0))/2*255)
	pygame.draw.ellipse(DISPLAYSURF, pygame.Color(col,col,col, col), (half[0] - 35, 400/2 - 64, 70, 23))
	pygame.draw.ellipse(DISPLAYSURF, black, (half[0] - 30, 400/2 - 65, 60, 20))


def renderConnectionDots(cons):
	ok = True
	for i in range(0,len(cons)):
		ind_col = white
		if(cons[i].status == False):
			ind_col = pygame.Color(255,50,50)
		elif(cons[i].ping > 30):
			ind_col = pygame.Color(255,255,50)
		pygame.draw.ellipse(DISPLAYSURF, ind_col, (10 + 30 * i, 10, 20, 20))
		if (cons[i].status == False or cons[i].serverUp == False):
			ok = False
			pygame.draw.ellipse(DISPLAYSURF, pygame.Color(0,0,0), (12 + 30 * i, 12, 16, 16))
	return ok
