import os
import web
import json

path = 'images'
paths = []


def getGifPaths():
    gifPaths = []
    for filename in os.listdir(path):
            currentPath = filename + '/compiled.gif'
            if(os.path.exists('images/' + currentPath)):
                gifPaths.append(currentPath)
            else:
                print('gif not found in folder ')
    return gifPaths


class Gallery:
    def GET(self):
        global paths
        paths = getGifPaths()
        web.header('Content-Type', 'text/html')
        render = web.template.render('gallery/')
        jsonPaths = json.dumps(paths)
        print(jsonPaths)
        return render.gallery(paths)

class GetImage:
    def GET(self, path, name):
        ext = name.split(".")[-1] # Gather extension
        cType ={
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
        }
        print('images/' + path + '/' + name)
        if name in os.listdir('images/' + path):  # Security
            #web.header("Content-Type", 'text/html') # Set the Header
            #return 'images/' + path + '/' + name
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/' + path + '/' + name, "rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()


# for filename in glob.glob(os.path.join(path, '*.txt')):
#     # do your stuff
