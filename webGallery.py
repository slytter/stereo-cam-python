import os
import web
import json
import gallery

paths = []

cType = {
	"png":"images/png",
	"jpg":"images/jpeg",
	"gif":"images/gif",
}

class Gallery:
	def GET(self):
		global paths
		paths = gallery.getImagePaths()
		web.header('Content-Type', 'text/html')
		render = web.template.render('gallery/')
		jsonPaths = json.dumps(paths)
		print(jsonPaths)
		return render.gallery(paths)

class GetImage:
	def GET(self, path):
		name = 'compiled.gif'
		ext = name.split(".")[-1] # Gather extension

		if(os.path.exists('images/' + path + '/compiled.gif')): 
			print('Serving existing gif')
		else:
			print('Gif not found. Compiling jpgs')
			gif = gallery.createGifFromPath('images/' + path)
			if(gif == False):
				raise web.notfound()
			web.header("Content-Type", cType[ext]) 
			return gif
			
		print('nam:' + name)
		print('images/' + path + '/' + name)
		if name in os.listdir('images/' + path):  # Security
			web.header("Content-Type", cType[ext]) # Set the Header
			return open('images/' + path + '/' + name, "rb").read() # Notice 'rb' for reading images
		else:
			raise web.notfound()


