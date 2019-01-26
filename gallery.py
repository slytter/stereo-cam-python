import threading
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
	thumps.currentPath = 0
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
	GUI.displayImage(image, thumps.currentPath)
	pygame.time.wait(50)

def getThumpnailPaths():
	gifPaths = []
	for filename in os.listdir(imagePath):
		currentPath = filename + '/thump/' 
		if(os.path.exists('images/' + currentPath + '0.jpg')):
			gifPaths.append(currentPath)
	return gifPaths


def createGifFromPath(path):
	numpyBuffer = []
	print('input path: ' + path)

	try:
		# for image in os.listdir(path):
		zigZag = sequenceGen.zigZag(len(numpyBuffer))

		for image in os.listdir(path):
			ext = image.split(".")[-1] # Gather extension
			if(ext == 'jpg'):
				imageRelPath = path + '/' + image
				print('appending image path: ' + imageRelPath)
				numpyBuffer.append(imageio.imread(imageRelPath))

		gif = imageio.mimwrite(imageio.RETURN_BYTES, numpyBuffer, format='gif', fps=_fps)
		name = path + '/compiled.gif'
		threading.Thread(target=saveImage, args=[gif, name]).start() # save image in thread.
		return gif # and serve the buffer to client in the mean time.
	except Exception as e:
		print('could not compile gifs Error: ' + str(e))
		return False


def saveImage(gif, name): 
	with open(name, 'wb') as f:
		f.write(gif)
		print(name + ': image saved!')


def getImagePaths():
	gifPaths = []
	for filename in os.listdir(imagePath):
		currentPath = filename + '/'
		if(os.path.exists('images/' + currentPath + '/0.jpg') or os.path.exists('images/' + currentPath + '/compiled.gif')): #only serve images where at least 1 image is present.
			gifPaths.append(currentPath)
			# else:
			# 	print('picture folder is empty ')
	return gifPaths