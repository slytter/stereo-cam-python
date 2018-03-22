import imageio
import requests
import datetime, time
import os

def downloadAndTakeImages(downloads, _fps) :
    paths = []
    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    basePath = 'images/' + str(timeStamp)
    os.makedirs(basePath)



# is sync... should be async: https://stackoverflow.com/questions/18377475/asynchronously-get-and-store-images-in-python
# second answer using grequest
    for i in range(0,len(downloads)) :
        img_data = requests.get(downloads[i]).content
        print("requesting image")
        path = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
        paths.append(path)
        with open(path, 'wb') as handler:
            handler.write(img_data)
            print("writing image")

    images = []
    for filename in paths:
        images.append(imageio.imread(filename))

    imageio.mimsave(basePath + '/compiled.gif', images,fps=_fps)

download = ['http://localhost:3000', 'http://192.168.0.34:3000']
downloadAndTakeImages(download, 10)
