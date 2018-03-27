import connections
from connections import Connection
from downloadImages import downloadImages 
import time
import RPi.GPIO as GPIO

status = False
pingAccuracy = 4
# realIps = ['http://localhost:3000', 'http://192.168.0.34:3000']
# realIps = ['slave1.local', 'master.local']

cons = []

cons.append(Connection('http://master.local', ':8080/capture'))
cons.append(Connection('http://slave1.local', ':8080/capture'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/embodied.jpg'))
#cons.append(Connection('http://slytter.tk', '/photos/project-images/lux.jpg'))

status = connections.pingConnections(cons, pingAccuracy)


def connectAndDownload():
	started = time.time()
	print('Starting requests')
	if(downloadImages(cons, 10)):
		print('Succesfully downloaded and compiled. It took: ' + str(time.time()-started) + ' secs')
	else:
		print('Download error. Re-pinging slaves')
		global status
		status = connections.pingConnections(cons, pingAccuracy)

# Pin Definitons:
pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
ledPin = 27# Broadcom pin 23 (P1 pin 16)
butPin = 17 # Broadcom pin 17 (P1 pin 11)

dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)
pwm.start(dc)



print("Here we go! Press CTRL+C to exit")
try:
	while 1:
		if GPIO.input(butPin): # button is released
			pwm.ChangeDutyCycle(dc)
			GPIO.output(ledPin, GPIO.LOW)
		else: # button is pressed:
			pwm.ChangeDutyCycle(100-dc)
			GPIO.output(ledPin, GPIO.HIGH)
			connectAndDownload()
			GPIO.output(ledPin, GPIO.HIGH)
			time.sleep(0.075)
			GPIO.output(ledPin, GPIO.LOW)
			
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	pwm.stop() # stop PWM
	GPIO.cleanup() # cleanup all GPIO