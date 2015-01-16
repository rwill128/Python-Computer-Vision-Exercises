from PIL import Image
from matplotlib import *
from numpy import *
from pylab import *
from scipy.ndimage import filters

image = array(Image.open('data/empire.jpg'))
image2 = filters.gaussian_filter(image, 5)
figure()
imshow(image)
figure()
imshow(image2)
show()