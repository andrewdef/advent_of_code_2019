import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

image_data = []
with open('input.txt') as fd:
	image_data = [int(x) for x in fd.read()]

image_size = IMAGE_HEIGHT * IMAGE_WIDTH	
number_of_layers = int(len(image_data) / image_size)

final_image = []

for k in range(0, image_size):
	winning_pixel = 2
	
	for i in range(0, number_of_layers):
		index = (i * image_size) + k
		c = image_data[index]
		
		if c in (0, 1):
			winning_pixel = c
			break			
		
	final_image.append(winning_pixel)
	
plt.imsave('filename.png', np.array(final_image).reshape(IMAGE_HEIGHT, IMAGE_WIDTH), cmap=cm.gray)
