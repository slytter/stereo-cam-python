import imageio
import requests
import datetime, time
import os

def downloadAndTakeImages(downloads, _fps) :
    paths = []
    timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    basePath = 'images/' + str(timeStamp)
    os.makedirs(basePath, exist_ok=True)



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

download = ['https://i1.sndcdn.com/artworks-000319237989-ooxmoa-t500x500.jpg', 'https://i1.sndcdn.com/artworks-000319389714-9u4dgh-t500x500.jpg']
downloadAndTakeImages(download, 10)