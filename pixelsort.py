from PIL import Image
import numpy as np


def hue(x):
	r = x[0] / 255
	g = x[1] / 255
	b = x[2] / 255
	Cmax = max(r, g, b)
	Cmin = min(r, g, b)
	delta = Cmax - Cmin

	if delta == 0:
		hue = 0
	elif Cmax == r:
		hue = 60 * (((g-b)/delta)%6)
	elif Cmax == g:
		hue = 60 * ((b-r)/delta + 2)
	else:
		hue = 60 * ((r-g)/delta + 4)
	return hue

def lightness(x):
	r = x[0] / 255
	g = x[1] / 255
	b = x[2] / 255
	Cmax = max(r, g, b)
	Cmin = min(r, g, b)
	
	return (Cmax + Cmin) / 2

def saturation(x):

	r = x[0] / 255
	g = x[1] / 255
	b = x[2] / 255
	Cmax = max(r, g, b)
	Cmin = min(r, g, b)
	delta = Cmax - Cmin

	if delta == 0:
		sat = 0
	else:
		sat = delta / (1 - abs(2 * lightness(x) - 1))

	return sat


mode = {
	'sum-rgb': lambda x: x[0] + x[1] + x[2],	# sort by sum of rgb values (grayscale)
	'red': lambda x: x[0],	# sort by red value
	'green': lambda x: x[1],	# sort by green value
	'blue': lambda x: x[2],	# sort by blue value
	'yellow': lambda x: x[0] + x[1], # sort by yellow value
	'cyan': lambda x: x[1] + x[2], # sort by cyan value
	'magenta': lambda x: x[0] + x[2], #sort by magenta value
	'luma': lambda x: 0.02126 * x[0] + 0.7152 * x[1] + 0.0722 * x[2], # sort by human color perception (luminosity)
	'hue': hue,
	'saturation': saturation,
	'lightness': lightness

}

def pixelsort(image_name, mode, row=True, reverse=False, start=lambda x: False, stop=lambda x: False):
	
	# PARAMETERS
	# image_name: name of image file
	# mode: mode to sort by
	# row: sort rows if True, otherwise sort by columns
	# reverse: sort in reverse if True

	picture = Image.open(image_name)

	if row: # convert numpy array to regular python list
		pixels = np.array(picture).tolist()
	else:
		# if you want to sort columns instead of row, just flip the image over its diagonal
		pixels = np.array(picture).transpose((1, 0, 2)) 
		print(pixels.shape)
		pixels = pixels.tolist()
	new_pixels = []

	for y in pixels:
		
		# sort each row (or column)
		index_start = index_of_first(y, 0, start)
		if index_start < 0:
			index_start = 0
		index_stop = index_of_first(y, index_start + 1, stop)
		if index_stop < 0:
			index_stop = len(y)

		segment_to_sort = y[index_start:index_stop]
		segment_to_sort.sort(key=mode, reverse=reverse)
		new_pixels.append(y[:index_start] + segment_to_sort + y[index_stop:])

	new_pixels = np.asarray(new_pixels, dtype='uint8')
	if not row:
		# flip back over the diagonal if sorting by columns
		new_pixels = new_pixels.transpose((1, 0, 2)) 

	# convert back to image
	im = Image.fromarray(new_pixels, 'RGB')
	im.show()

	return im

def index_of_first(arr, index, predicate):
	for i in range(index, len(arr)):
		if predicate(arr[i]):
			return i
	return -1

def save_as(image, name='sorted.jpg'):
	image.save(name)




start = lambda x: x[0] + x[1] + x[2] < 360
stop = lambda x: x[0] + x[1] + x[2] > 360


# image = pixelsort('cloud.jpg', mode['luma'], row=False, reverse=True)
image = pixelsort('paint.png', mode['lightness'], row=False, reverse=True)

# image = pixelsort('einstein.jpg', lambda, True) # 'sort image's rows by red'
# save_as(image, 'pixelsorted3.jpg')






# image = pixelsort('image.jpg', mode['red'], True)
# save_as(image, 'pixelsort.jpg')