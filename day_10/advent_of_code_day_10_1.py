def has_los(asteroid_1, asteroid_2):
	x1 = asteroid_1[0]
	x2 = asteroid_2[0]
	
	y1 = asteroid_1[1]
	y2 = asteroid_2[1]
	
	if x1 == x2 and y1 == y2:
		return False
	
	if x1 != x2:	
		if x1 < x2:
			start = x1 + 1
			stop = x2
			step = 1
		else:
			start = x1 - 1
			stop = x2
			step = -1
			
		for x in range(start, stop, step):
			y = (((x - x1)/(x2 - x1))*(y2 - y1)) + y1
			
			if y == int(y):
				if grid[int(y)][x] == True:
					return False
	if y1 != y2:		
		if y1 < y2:
			start = y1 + 1
			stop = y2
			step = 1
		else:
			start = y1 - 1
			stop = y2
			step = -1
		
		for y in range(start, stop, step):
			x = (((y - y1)/(y2 - y1))*(x2 - x1)) + x1
			if x == int(x):
				if grid[y][int(x)] == True:
					return False
		
	return True
	
asteroids = []
grid = []
with open('input.txt') as fd:
	i = 0
	for line in fd.readlines():
		k = 0
		grid_line = []
		for c in line:
			if c == '#':
				asteroids.append((k, i))
				grid_line.append(True)
			else:
				grid_line.append(False)
				
			k = k + 1
		
		grid.append(grid_line)
		i += 1

max_visible_asteroids = 0
champion = None
for asteroid_1 in asteroids:
	num_of_visible_asteroids = 0
	
	for asteroid_2 in asteroids:
		if has_los(asteroid_1, asteroid_2):
			num_of_visible_asteroids += 1
			
	if num_of_visible_asteroids > max_visible_asteroids:
		champion = asteroid_1
		max_visible_asteroids = num_of_visible_asteroids
	
print(max_visible_asteroids)
print(champion)