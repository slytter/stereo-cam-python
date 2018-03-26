import web
import io
import time
from PIL import Image
#import picamera

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

        input = web.input(w="0", h="0",delay="0")                 # reading user input of resolution values for 

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

        #camera = picamera.PiCamera()                    # camera
        #camera.capture('picture.jpg')                   # capture image to file
        #camera.close()
        print('It took ' + str(time.time()-startTime) + ' to init request (with or without delay)')
        # Create the in-memory stream
        stream = io.BytesIO()
        print('It took ' + str(time.time()-startTime) + ' to init buffer')
        with picamera.PiCamera() as camera:
            print('It took ' + str(time.time()-startTime) + ' to init camera')
            camera.resolution = (input.w, input.h)
            camera.start_preview()
            print('It took ' + str(time.time()-startTime) + ' to set res and preview')

            time.sleep(1)
            camera.capture(stream, format='jpeg')
            print('It took ' + str(time.time()-startTime) + ' to capture into stream (with preview sleep time)')

        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        web.header('Content-Type', 'image/jpg')
        print('It took ' + str(time.time()-startTime) + ' to finish')
        return stream.read()
        #return open('0.jpg',"rb").read()          # read image from file and respond
