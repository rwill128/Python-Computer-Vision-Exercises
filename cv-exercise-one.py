from PIL import Image
from matplotlib import *
from numpy import *
from pylab import *

image = array(Image.open('data/empire.jpg'))

imshow(image)
x = [100,100,400,400]
y = [200,500,200,500]

plot(x,y,'r*')

plot(x[:2],y[:2])

title('Plotting: "empire.jpg"')
show()