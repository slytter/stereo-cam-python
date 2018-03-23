import connections
from connections import Connection
from downloadImages import downloadImages 
status = False
pingAccuracy = 3
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']

cons = []
cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, pingAccuracy)

if(downloadImages(cons, 10)):
	print('Succesfully downloaded and compiled')
else: 
	print('Download error. Re-pinging slaves')
	status = False
	status = connections.pingConnections(cons, pingAccuracy)

