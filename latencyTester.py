import os, sys, pexpect, time, datetime

def averagePing(ping_destination, amount) :
	# SET YOUR PING RESPONSE TIME THRESHOLD HERE, IN MILLISECONDS
	threshold = 1250
	interval = 0.25
	ping_destination = ping_destination.replace("http://","") # removing http:// from the string since its not supported in ping
	count = 0
	line = 'Ping Interval: ' + str(interval) + ', Destination: ' + ping_destination + ', Threshold to Log (msec): ' + str(threshold) + '\n'
	ping_command = 'ping -i ' + str(interval) + ' ' + ping_destination

	child = pexpect.spawn(ping_command)
	child.timeout=1200

	pings = []
 
	while 1:
		line = child.readline()
		if not line:
			return False

		if line.startswith(b'ping: unknown host'):
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
