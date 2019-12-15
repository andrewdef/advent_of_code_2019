IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

image_data = []
with open('input.txt') as fd:
	image_data = [int(x) for x in fd.read()]
	
number_of_layers = int(len(image_data) / (IMAGE_HEIGHT * IMAGE_WIDTH))

images = {}
min_number_of_zeros = None
answer = None

for i in range(0, number_of_layers):
	layer = {}
	for k in range(0, (IMAGE_HEIGHT * IMAGE_WIDTH)):
		index = (i * (IMAGE_HEIGHT*IMAGE_WIDTH)) + k
		c = image_data[index]
		
		if layer.get(c) == None:
			layer[c] = 0
			
		layer[c] += 1
		
	images[i] = layer
	
	if min_number_of_zeros == None or layer[0] < min_number_of_zeros :
		answer = layer[1] * layer[2]
		min_number_of_zeros = layer[0]
		
print(answer)
	
