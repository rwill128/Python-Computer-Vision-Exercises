from PIL import Image
from matplotlib import *
from numpy import *
from pylab import *
from scipy.ndimage import filters

image = array(Image.open('data/empire.jpg').convert('L'))

sigma = 5

imageX = zeros(image.shape)
filters.gaussian_filter(image, (sigma, sigma), (0,1), imageX)

imageY = zeros(image.shape)
filters.gaussian_filter(image, (sigma, sigma), (1,0), imageY)

magnitude = sqrt(imageX**2+imageY**2)

gray()

figure()
imshow(image)

figure()
imshow(imageX)

figure()
imshow(imageY)

figure()
imshow(magnitude)

show()