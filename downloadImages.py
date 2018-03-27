import imageio
import datetime, time, os
import grequests
import time
from start import turnOffLED
def downloadImages(cons, _fps) :
	startTime = time.time()
	paths = []

	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
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
	starting = time.time()
	for response in responses:
		if 199 < response.status_code < 400:
			name = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
			paths.append(name)
			with open(name, 'wb') as f:
				f.write(response.content)
		else:
			return False
		i += 1
	print('It took ' + str(time.time()-startTime) + 'to download images')
	turnOffLED()
	images = []
	for filename in paths:
		images.append(imageio.imread(filename))
	imageio.mimsave(basePath + '/compiled.gif', images, fps=_fps)
	return True
