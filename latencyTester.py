import os, sys, time, datetime
import socket


def online(ping_destination):
	ping_destination = ping_destination.replace("http://","")
	HOST_UP = True if os.system("timeout 5 ping -c 1 -W 5 " + ping_destination) is 0 else False
	return HOST_UP

def averagePing(ping_destination, amount) :
	# SET YOUR PING RESPONSE TIME THRESHOLD HERE, IN MILLISECONDS
	threshold = 1250
	interval = 0.25
	ping_destination = ping_destination.replace("http://","") # removing http:// from the string since its not supported in ping
	count = 0
	line = 'Ping Interval: ' + str(interval) + ', Destination: ' + ping_destination + ', Threshold to Log (msec): ' + str(threshold) + '\n'
	ping_command = 'ping ' + ping_destination + ' -t 1'

	# child = pexpect.spawn(ping_command)
	child.timeout=400

	pings = []
 
	while 1:
		line = child.readline()
		if not line:
			return False

		if line.startswith(b'ping: unknown host'):
			print('Unknown host: ' + ping_destination)
			return False

		if line.startswith(b'Alarm clock:'):
			print('Unknown host: ' + ping_destination)
			return False

		if count > 0:
			ping_time = float(line[line.find(b'time=') + 5:line.find(b' ms')])
			line = time.strftime("%m/%d/%Y %H:%M:%S") + ": " + str(ping_time)
			#print(str(count) + ": " + line)
			pings.append(ping_time)
			if ping_time > threshold:
				print('Ping over threshold, disrupting.')
		if(count >= amount):
			return sum(pings) / float(len(pings))
		count += 1
