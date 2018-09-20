import os, platform, time
import shlex  
from latencyTester import averagePing, online
from subprocess import Popen, PIPE, STDOUT
import grequests
import asyncio
import GUI
import time
# from runcoroutine import runCoroutine
_mayCheckConnections = True
def enableConnectionCheck(enable):
	mayCheckConnections = enable
def mayCheckConnection():
	return _mayCheckConnections

class Connection : # place this in another doc please..
	ip = ''
	port = ''
	ping = 0
	status = False
	serverUp = False
	reversedPing = 0
	def __init__ (self, _ip, _port):
		self.ip = _ip
		self.port = _port
	
	def updateConnection(self, accuracy):
		con = online(self.ip)
		print(self.ip)
		if(con != False) : # returning false if connection down, and the ping if up
			self.ping = con
			self.status = True
			print('Ping connection up for ' + self.ip + ' with ping: ' + str(self.ping))
			return True
		else : 
			self.status = False
			print('Ping connection could not be established to ' + self.ip)
			return False


def arePisConnected(cons, accuracy, loop = True):
	print('Trying to ping-connect to slaves')
	for connection in cons :
		if(mayCheckConnection() == False):
			break
		connection.updateConnection(accuracy)

def checkClientStatus(cons):
	ips = map(lambda con: con.ip + con.port + 'status', cons) # reversed pings instead of pings
	requests = (grequests.get(ip, timeout = 0.5) for ip in ips)
	responses = grequests.map(requests)
	for i in range(0, len(cons)):
		if(responses[i] != None and responses[i].status_code == 200):
			cons[i].status = True # status is ping connectivity, which must be up in this case.
			cons[i].serverUp = True
		else:
			cons[i].serverUp = False


def updateConnections(cons, eachSeconds): # This function is ran outside the main thread. As a background connectivity check
	try:
		while 1: # Constantly check
			if(mayCheckConnection()): # if permitted
				checkClientStatus(cons) # and that the slave servers are up and returning 200
				
				# if the servers are down. The pi might be shut. Lets ping the disconnected pis:
				disconnectedPis = list(filter(lambda x: x.serverUp == False, cons))
				if(len(disconnectedPis) > 0):
					print('Could not connect to ' + str(len(disconnectedPis)) + ' server(s). Trying to ping')
					arePisConnected(disconnectedPis, 1, False) # that the pi's can be seen on the network.

				time.sleep(eachSeconds) # then wait for a while
			else: # if not permitted
				time.sleep(1) # check again in 1 sec.
	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
		GPIO.cleanup() # cleanup all GPIO


def shutDownPis(cons):
	ips = map(lambda con: con.ip + con.port + 'shutdown', cons[1:]) 
	# print('shutting down ' + len(ips) + ' connections')
	for ip in ips:
		print('shutting down ' + ip)
	requests = (grequests.get(ip, timeout = 0.5) for ip in ips)
	responses = grequests.map(requests)
	GUI.message('shutting down camera')
	print('shutting master in 5 seconds')
	time.sleep(5)
	os.system('sudo shutdown now')