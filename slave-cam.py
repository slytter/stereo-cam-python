import web
import io
import time
from PIL import Image
import picamera
import RPi.GPIO as GPIO

readyPin = 15
shutterInput = 14
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
#pwm = GPIO.PWM(pwmPin, 100)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(shutterInput, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(readyPin, GPIO.OUT) # LED pin set as output
GPIO.output(readyPin, GPIO.LOW)




urls = (
    '/capture', 'Capture'
)

# start with default values for resolution
width = 1024
height = 1024

if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()

class Capture:
    def GET(self):
        startTime = time.time()

        input = web.input(w="0", h="0", delay="0")      # reading user input of resolution values for 

        input.w = int(input.w)                          # to integer
        input.h = int(input.h)
        input.delay = float(input.delay)

        

        if(input.delay != 0):
            print('delaying image caputure by' + str(input.delay))
            time.sleep(input.delay/1000)

        if input.w == 0:
            input.w = width                             # no width given, use saved one
        else:
            input.w = max(0,min(2592, input.w))         # clamp to range of valid values

        if input.h == 0:
            input.h = height                            # no height given, use saved one
        else:
            input.h = max(0,min(1944, input.h))         # clamp to range of valid values

        print('It took ' + str(time.time()-startTime) + ' to init request (with or without delay)')
        stream = io.BytesIO()
        print('It took ' + str(time.time()-startTime) + ' to init buffer')
        with picamera.PiCamera() as camera:
            print('It took ' + str(time.time()-startTime) + ' to init camera')
            camera.rotation = 180
            camera.resolution = (input.w, input.h)
            camera.start_preview()
            print('It took ' + str(time.time()-startTime) + ' to set res and preview')

            #time.sleep(1.0 - (time.time()-startTime)) # delay compensation is withheld from the camera focus time
            imageCaptured = False
            GPIO.output(readyPin, GPIO.HIGH)
            try:
                while imageCaptured == False:
                    if  (GPIO.input(shutterInput) == True): # button is released
                        GPIO.output(readyPin, GPIO.LOW)  
                        print('button is released.')
                        camera.capture(stream, format='jpeg')
                        imageCaptured = True
                        GPIO.output(readyPin, GPIO.HIGH)
                        time.sleep(0.05)
                        GPIO.output(readyPin, GPIO.LOW)  
                        break
#                    else: # button is pressed:
#                        print('awaiting button release')
            except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
                GPIO.cleanup() # cleanup all GPIO
                pwm.stop() # stop PWM
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        web.header('Content-Type', 'image/jpg')
        print('It took ' + str(time.time()-startTime) + ' to finish')
        return stream.read()
