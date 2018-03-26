import web
import io
import time
from PIL import Image
import picamera

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
        input = web.input(w="0", h="0",delay="0")                 # reading user input of resolution values for 

        input.w = int(input.w)                          # to integer
        input.h = int(input.h)
        input.delay = int(input.delay)

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

        # Create the in-memory stream
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution = (input.w, input.h)
            camera.start_preview()
            time.sleep(1)
            camera.capture(stream, format='jpeg')
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        web.header('Content-Type', 'image/jpg')
        return stream.read()
        #return open('0.jpg',"rb").read()          # read image from file and respond
