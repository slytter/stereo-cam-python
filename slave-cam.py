import web, socket
import io
import time
import picamera
import RPi.GPIO as GPIO

master = (socket.gethostname() == 'master' or socket.gethostname() == 'master2' )

readyPin = 15
shutterInput = 14

if(master):
    print('running server as master')
    import webGallery
    from webGallery import Gallery, GetImage
    import os
    readyPin = 26
    shutterInput = 19



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
#pwm = GPIO.PWM(pwmPin, 100)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(shutterInput, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
GPIO.setup(readyPin, GPIO.OUT) # LED pin set as output

ok = False


urls = (
    '/capture', 'Capture',
    '/status', 'Status',
    '/update', 'Update',
    '/shutdown', 'Shutdown',
)

if(master):
    masterUrls = (
        '/gallery', 'Gallery',
        '/get-image/(.+)/', 'GetImage',
    )
    urls = urls + masterUrls



# start with default values for resolution
width = 1000
height = 1000

if __name__ == "__main__":
    app = web.application(urls, globals())
    GPIO.output(readyPin, GPIO.HIGH)
    time.sleep(0.15)
    GPIO.output(readyPin, GPIO.LOW)
    app.run()

ok = True
class Status:
    def GET(self):
        web.header('Content-Type', 'text/html')
        return str(ok)



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

        stream = io.BytesIO()
        print('Ready in ' + str(time.time()-startTime) + ' secs ')
        with picamera.PiCamera() as camera:
            print('Camera init took ' + str(time.time()-startTime) + ' secs')
            camera.rotation = 180
            camera.resolution = (input.w, input.h)
            camera.start_preview()
            print('preview now running after ' + str(time.time()-startTime) + ' secs')

            imageCaptured = False
            GPIO.output(readyPin, GPIO.HIGH)
            try:
                while imageCaptured == False:
                    if  (GPIO.input(shutterInput) == GPIO.HIGH): # button is released
                        GPIO.output(readyPin, GPIO.LOW) # illustrate ready state 
                        print('exp: 1/' + str(1000.0 / (camera.exposure_speed / 1000)))
                        camera.capture(stream, format='jpeg')
                        print('Button released, capturing...')
                        imageCaptured = True
                        GPIO.output(readyPin, GPIO.HIGH)
                        time.sleep(0.0005) # 1/2000 shutter time accuracy
                        GPIO.output(readyPin, GPIO.LOW)
                        break
                    # else:
                       #time.sleep(0.005) # 1/200 shutter time accuracy
            except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
                GPIO.cleanup() # cleanup all GPIO
                pwm.stop() # stop PWM
            except:
                pass
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        web.header('Content-Type', 'image/jpg')
        print('Done. It took ' + str(time.time()-startTime) + ' to capture image')
        return stream.read()


class Update:
    def GET(self):
        os.system('git pull && sudo reboot now')
        return "error could not restart"

class Shutdown:
    def GET(self):
        os.system('sudo shutdown')
