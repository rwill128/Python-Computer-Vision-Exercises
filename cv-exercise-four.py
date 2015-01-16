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

def get_harris_points(harrisImage, min_dist=50, threshold=0.2):

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

image = array(Image.open('data/empire.jpg').convert('L'))
 
imageHarris = compute_harris_response(image)
coords = get_harris_points(imageHarris)

print(coords)

plot_harris_points(imageHarris, coords)

figure()
imshow(image)

figure()
imshow(imageHarris)

show()