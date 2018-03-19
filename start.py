import imageio
import requests
import datetime, time
import os

def downloadAndTakeImages(downloads, _fps) :
    paths = []
    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    basePath = 'images/' + str(timeStamp)
    os.makedirs(basePath, exist_ok=True)

    for i in range(0,len(download)) :
        img_data = requests.get(download[i]).content
        path = 'images/' + str(timeStamp) + '/' + str(i) + '.jpg'
        paths.append(path)
        with open(path, 'wb') as handler:
            handler.write(img_data)

    images = []
    for filename in paths:
        images.append(imageio.imread(filename))

    imageio.mimsave(basePath + '/compiled.gif', images,fps=_fps)

download = ['https://i1.sndcdn.com/artworks-000319237989-ooxmoa-t500x500.jpg', 'https://i1.sndcdn.com/artworks-000319389714-9u4dgh-t500x500.jpg']
downloadAndTakeImages(download, 10)