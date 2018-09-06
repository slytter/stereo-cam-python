import os, platform, time
import shlex  
from latencyTester import averagePing
from subprocess import Popen, PIPE, STDOUT
import grequests
import asyncio
import GUI
from runcoroutine import runCoroutine

bool _mayCheckConnections = True
def enableConnectionCheck(enable):
	mayCheckConnections = enable
def mayCheckConnection():
	return _mayCheckConnections

class Connection : # place this in another doc please..
	ip = ''
	port = ''
	ping = 0
	status = False
	reversedPing = 0
	serverUp = False
	def __init__ (self, _ip, _port):
		self.ip = _ip
		self.port = _port
	
	def updateConnection(self, accuracy):
		con = averagePing(self.ip, accuracy)
		if(con != False) : # returning false if connection down, and the ping if up
			self.ping = con
			self.status = True
			print('Connection up for ' + self.ip + ' with ping: ' + str(self.ping))
			return True
		else : 
			self.status = False
			print('Connection could not be established to ' + self.ip)
			return False


def pingConnections(cons, accuracy, loop = True):
	anyConnectionDown = 1
	longestPing = 0
	while (anyConnectionDown > 0) :
		print('Trying to connect to slaves')
		anyConnectionDown = 0

		for connection in cons :
			if(connection.updateConnection(accuracy) == False):
				anyConnectionDown += 1
			else:
				if connection.ping > longestPing :
					longestPing = connection.ping
		
		if(anyConnectionDown > 0):
			GUI.loadingScreen(str(anyConnectionDown) + ' connection' + ('' if(anyConnectionDown == 1) else 's') + ' down')
			#checkClientStatus(cons)
			GUI.renderConnectionDots(cons)
			GUI.pygame.display.update()
			if(loop == False):
				pingConnections = 0 #thus breaking the while loop
			else:
				print(str(anyConnectionDown) + ' connection down. Re-pinging in 1 second')
				time.sleep(1)
		else:
			print('longest ping: ' + str(longestPing))
			for connection in cons:
				connection.reversedPing = longestPing - connection.ping #calculate reverse ping (largest_ping - ping for each ping in pings)
			return True
	return True



async def checkClientStatus(cons):
	ips = map(lambda con: con.ip + con.port + 'status', cons) # reversed pings instead of pings
	requests = (grequests.get(ip, timeout = 0.5) for ip in ips)
	responses = grequests.map(requests)
	for i in range(0, len(cons)):
		if(responses[i] != None and responses[i].status_code == 200):
			cons[i].serverUp = True
		else:
			cons[i].serverUp = False
#		print(cons[i].serverUp)
#		print(cons[i].ip)



