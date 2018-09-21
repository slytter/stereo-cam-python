import os
import web
import json
import glob
import imageio

imagePath = 'images'
paths = []
_fps = 10

cType = {
	"png":"images/png",
	"jpg":"images/jpeg",
	"gif":"images/gif",
}

def getImagePaths():
	gifPaths = []
	for filename in os.listdir(imagePath):
			currentPath = filename + '/'
			if(os.path.exists('images/' + currentPath + '/0.jpg') or os.path.exists('images/' + currentPath + '/compiled.gif')): #only serve images where at least 1 image is present.
				gifPaths.append(currentPath)
			# else:
			# 	print('picture folder is empty ')
	return gifPaths




class Gallery:
	def GET(self):
		global paths
		paths = getImagePaths()
		web.header('Content-Type', 'text/html')
		render = web.template.render('gallery/')
		jsonPaths = json.dumps(paths)
		print(jsonPaths)
		return render.gallery(paths)

class GetImage:
	def GET(self, path):

		if(os.path.exists('images/' + path + '/compiled.gif')): 
			print('Serving existing gif')
		else:
			print('Gif not found. Compiling jpgs')
			OK = createGifFromPath('images/' + path)
			if(OK == False):
				raise web.notfound()
			
		name = 'compiled.gif'
		ext = name.split(".")[-1] # Gather extension
		print('nam:' + name)
		print('images/' + path + '/' + name)
		if name in os.listdir('images/' + path):  # Security
			web.header("Content-Type", cType[ext]) # Set the Header
			return open('images/' + path + '/' + name, "rb").read() # Notice 'rb' for reading images
		else:
			raise web.notfound()


def createGifFromPath(path):
	numpyBuffer = []
	print('input path: ' + path)
	try:	
		for image in os.listdir(path):
			ext = image.split(".")[-1] # Gather extension
			if(ext == 'jpg'):
				imageRelPath = path + '/' + image
				print('appending image path: ' + imageRelPath)
				numpyBuffer.append(imageio.imread(imageRelPath))
		imageio.mimsave(path + '/compiled.gif', numpyBuffer, fps=_fps)
		return True
	except Exception as e:
		print('could not compile gifs Error: ' + str(e))
		return False

