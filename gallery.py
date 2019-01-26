import sequenceGen
import imageio
import os
import pygame
import GUI
import time

_fps = 10
imagePath = 'images'
class Thumps():
	currentPath = 0
	paths = []
	currentBuffer = []
	gifIndex = 0

thumps = Thumps()


def setup():
	print('setup')
	thumps.paths = getThumpnailPaths()
	thumps.currentPath = len(thumps.paths)-1
	loadImage()


def loadImage():
	thumps.currentBuffer = []
	path = "images/" + thumps.paths[thumps.currentPath]
	for image in os.listdir(path):
		print(image)
		ext = image.split(".")[-1] # Gather extension
		if(ext == 'jpg'):
			thumps.currentBuffer.append(pygame.image.load(os.path.join(path, image))) 


def switchImage(direction):
	thumps.currentPath += direction
	thumps.currentPath = min(thumps.currentPath, len(thumps.paths)-1)
	thumps.currentPath = max(thumps.currentPath, 0)
	loadImage()

def draw():
	zigZag = sequenceGen.zigZag(len(thumps.currentBuffer))
	image = thumps.currentBuffer[zigZag[thumps.gifIndex % len(zigZag)]]
	thumps.gifIndex += 1
	GUI.displayImage(image, str(thumps.currentPath+1) + '/' + str(len(thumps.paths)))
	pygame.time.wait(50)

def getThumpnailPaths():
	gifPaths = []
	for filename in os.listdir(imagePath):
		currentPath = filename + '/thump/' 
		if(os.path.exists('images/' + currentPath + '0.jpg')):
			gifPaths.append(currentPath)
	return sorted(gifPaths)


