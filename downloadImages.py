import imageio
import datetime, time, os
import grequests
import time
import RPi.GPIO as GPIO

lastImagePath = ""

def getLastImagePath():
	return lastImagePath
	
def downloadImages(cons, _fps) :
	startTime = time.time()
	paths = []

	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
	basePath = 'images/' + str(timeStamp)
	os.makedirs(basePath)

	print('Requesting')
	ips = map(lambda con: con.ip + con.port + '?delay=' + str(con.reversedPing), cons) # reversed pings instead of pings
#	for ip in ips:   
#		print(ip)

	requests = (grequests.get(ip, timeout = 10) for ip in ips)
	responses = grequests.map(requests)
	for response in responses:
		print(response)
	i = 0 
	frameCache = []
	starting = time.time()
	for response in responses:
		if 199 < response.status_code < 400:
			name = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
			global lastImagePath
			lastImagePath = name
			paths.append(name)
			with open(name, 'wb') as f:
				frameCache.append(response.content)
				f.write(response.content) # TODO SAVE THIS IN A BUFFER INSTEAD OF WRITING AND READING TO COMPILE GIF
		else:
			return []
		i += 1
	print('It took ' + str(time.time()-startTime) + 'to download images')
	GPIO.output(27, GPIO.LOW)
	images = []
	#for filename in paths:
	#images.append(imageio.imread(filename))
	#imageio.mimsave(basePath + '/compiled.gif', images, fps=_fps)
	return frameCache
