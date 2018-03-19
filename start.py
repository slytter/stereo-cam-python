print('smagen')
from io import BytesIO
import imageio

im = imageio.imread('http://upload.wikimedia.org/wikipedia/commons/d/de/Wikipedia_Logo_1.0.png')  # read a standard image

filenames = ['test.jpg', 'test2.png']

images = []
for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimsave('movie.gif', images)
