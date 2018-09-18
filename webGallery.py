import os
import web
import json

path = 'images'
paths = []


def getGifPaths():
	gifPaths = []
	for filename in os.listdir(path):
			currentPath = 'images/' + filename + '/0.jpg'
			if(os.path.exists(currentPath)):
				gifPaths.append(currentPath)
				print(currentPath)
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
		return render.gallery(jsonPaths)

class GetImage:
	def GET(self):
		web.header('Content-Type', 'text/html')
		return 'getImage'

# for filename in glob.glob(os.path.join(path, '*.txt')):
#     # do your stuff
