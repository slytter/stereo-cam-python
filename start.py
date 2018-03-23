import connections
from connections import Connection
from downloadImages import downloadImages 
import time
status = False
pingAccuracy = 3
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']

cons = []
cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, pingAccuracy)

def connectAndDownload():
	if(downloadImages(cons, 10)):
		print('Succesfully downloaded and compiled')
	else: 
		print('Download error. Re-pinging slaves')
		global status 
		status = connections.pingConnections(cons, pingAccuracy)
		connectAndDownload()

# should be threaded or async
def loop():
	time.sleep(1)
	print('loop')
	loop()

loop()