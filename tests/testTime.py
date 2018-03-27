import time
import datetime

def loop():
	timeS = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')[:-3]
	print(timeS)
	time.sleep(0.01)
	loop()
loop()

