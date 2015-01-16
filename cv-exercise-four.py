from PIL import Image
from matplotlib import *
from numpy import *
from pylab import *
from scipy.ndimage import filters

def compute_harris_response(image, sigma=3):
	imageX = zeros(image.shape)
	filters.gaussian_filter(image, (sigma, sigma), (0,1), imageX)

	imageY = zeros(image.shape)
	filters.gaussian_filter(image, (sigma, sigma), (1,0), imageY)

	Wxx = filters.gaussian_filter(imageX*imageX, sigma)
	Wxy = filters.gaussian_filter(imageX*imageY, sigma)
	Wyy = filters.gaussian_filter(imageY*imageY, sigma)

	Wdet = Wxx*Wxy - Wxy**2
	Wtr = Wxx + Wyy

	return Wdet / Wtr;

def get_harris_points(harrisImage, min_dist=10, threshold=0.5):

	corner_threshold = harrisImage.max() * threshold
	harrisImage_t = (harrisImage > corner_threshold) * 1

	coords = array(harrisImage_t.nonzero()).T

	candidate_values = [harrisImage[c[0],c[1]] for c in coords]

	index = argsort(candidate_values)

	allowed_locations = zeros(harrisImage.shape)
	allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

	filtered_coords = [];

	for i in index:
		if allowed_locations[coords[i,0], coords[i,1]] == 1:
			filtered_coords.append(coords[i])
			allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
			(coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0

	return filtered_coords

def plot_harris_points(image, filtered_coords):
	figure()
	gray()
	imshow(image)
	plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords], '*')
	axis('off')

def plot_compare_points(image, filtered_coordsOne, filtered_coordsTwo):
	figure()
	gray()
	imshow(image)
	plot([p[1] for p in filtered_coordsOne], [p[0] for p in filtered_coordsOne], '*')
	plot([p[1] for p in filtered_coordsTwo], [p[0] for p in filtered_coordsTwo], '-')
	axis('off')

image = array(Image.open('data/empire.jpg').convert('L'))
 
sigma = 3

imageX = zeros(image.shape)
filters.gaussian_filter(image, (sigma, sigma), (0,1), imageX)

imageY = zeros(image.shape)
filters.gaussian_filter(image, (sigma, sigma), (1,0), imageY)

magnitude = sqrt(imageX**2+imageY**2)
magCoords = get_harris_points(magnitude)

imageHarris = compute_harris_response(image)
harrisCoords = get_harris_points(imageHarris)

plot_harris_points(imageHarris, harrisCoords)
plot_harris_points(magnitude, magCoords)
plot_compare_points(image, harrisCoords, magCoords)

show()