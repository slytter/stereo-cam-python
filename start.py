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

download = ['https://i1.sndcdn.com/artworks-000319237989-ooxmoa-t500x500.jpg', 'https://i1.sndcdn.com/artworks-000319389714-9u4dgh-t500x500.jpg']



class Connection : 
    ip = ''
    port = ''
    ping = 0
    status = False
    
    def __init__ (self, _ip, _port):
        self.ip = _ip
        self.port = _port
    
    def updateConnection(self) :
        connection = True
        newPing = 10
        if(self.ping == connection) : # psuedo check for ping and return true if connection up.
            self.ping = (self.ping + newPing) / 2 # moving average thing
            self.status = True
            print('Connection up for ' + self.ip + 'with ping: ' + self.ping)
            return True
        else : 
            self.status = False
            print('Connection could not be established to ' + self.ip)
            return False
        


connections = []
connections.append(Connection('https://i1.sndcdn.com/artworks-000319237989-ooxmoa-t500x500.jpg', '3000'))
connections.append(Connection('https://i1.sndcdn.com/artworks-000319389714-9u4dgh-t500x500.jpg', '3000'))


def checkPing(connections) : 
    for connection in connections :
        connection.updateConnection()
        

checkPing(connections)