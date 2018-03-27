import threading
import requests
import datetime, time
import os

results = []

paths = []
timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
basePath = 'images/' + str(timeStamp)
os.makedirs(basePath)

def getter(download, i):
    global paths, timeStamp, basePath
    print(download)
    img_data = requests.get(download).content
    print("requesting image")
    
    path = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
    paths.append(path)
    with open(path, 'wb') as handler:
        handler.write(img_data)
        print("writing image")

threads = []
images = []
images.append('http://master.local:8080/capture')
images.append('http://slave1.local:8080/capture')

for x in range(0,2):
    t = threading.Thread(target=getter, args=(images[x], x))
    t.start()
    threads.append(t)
# wait for all threads to finish
# You can continue doing whatever you want and
# join the threads when you finally need the results.
# They will fatch your urls in the background without
# blocking your main application.
map(lambda t: t.join(), threads)
