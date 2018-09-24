import imageio
import datetime, time, os
import grequests
import time
import RPi.GPIO as GPIO
from io import BytesIO
import threading

def downloadImages(cons, _fps) :
	startTime = time.time()
	paths = []

	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
	print(timeStamp)
	basePath = 'images/' + str(timeStamp)
	os.makedirs(basePath)

	print('Requesting')
	ips = map(lambda con: con.ip + con.port + 'capture', cons) # reversed pings instead of pings

	requests = (grequests.get(ip, timeout = 20) for ip in ips)
	responses = grequests.map(requests)
	for response in responses:
		print(response)
	i = 0 
	imageBuffers = []
	numpyBuffer = [] 
	starting = time.time()
	for response in responses:
		if (response and 199 < response.status_code < 400):
			name = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
			paths.append(name)
			imageBuffers.append(BytesIO(response.content))
			#numpyBuffer.append(imageio.imread(BytesIO(response.content)))
			#Thread this:
			# with open(name, 'wb') as f:
			# 	f.write(response.content) # TODO SAVE THIS IN A BUFFER INSTEAD OF WRITING AND READING TO COMPILE GIF

			threading.Thread(target=saveImage, args=[response.content, name]).start() 
			print('after thread is started.')
			#saveImage(response.content, name)
		else:
			return []
		i += 1
	print('It took ' + str(time.time()-startTime) + 'to download images')
	#imageio.mimsave(basePath + '/compiled.gif', numpyBuffer, fps=_fps)
	GPIO.output(27, GPIO.LOW)
	return imageBuffers

def saveImage(image, name): 
	print('from thread.')
	with open(name, 'wb') as f:
		f.write(image)
		print(name + ': image saved!')

def connectAndDownload(cons):
	started = time.time()
	print('Starting requests')
	frameBuffers = downloadImages(cons, 10)
	if(len(frameBuffers) != 0):
		print('Succesfully downloaded. It took: ' + str(time.time()-started) + ' secs (w/ focus)')
		return frameBuffers
	else:
		print('Download error')
		return False
			