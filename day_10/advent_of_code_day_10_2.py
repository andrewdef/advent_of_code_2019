import math
from operator import itemgetter, attrgetter, methodcaller

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
	
def calculate_angular_distance(center, p):
	relative_x = p[0] - center[0]
	relative_y = center[1] - p[1]
	
	distance = math.degrees(math.atan2(relative_x, relative_y))
	
	if distance < 0:
		return (360 + distance)
	else:
		return distance
	
def calculate_distance(center, p):
	relative_x = p[0] - center[0]
	relative_y = p[1] - center[1]
	
	return math.sqrt(relative_x ** 2 + relative_y ** 2)
	
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

targets = []
for target_asteroid in asteroids:
	angular_distance = calculate_angular_distance(champion, target_asteroid)
	distance = calculate_distance(champion, target_asteroid)
		
	if angular_distance != 0 or distance != 0:
		targets.append([angular_distance, distance, False, target_asteroid])

targets = sorted(targets, key=itemgetter(0, 1))

print(targets)

total_asteroid_destroyed = 0
answer = None

while( True ):
	asteroid_destroyed_in_this_sweep = 0
	
	previous_angle = -1
	for target in targets:
		current_angle = target[0]
		
		if target[2] == False and has_los(champion, target[3]) and current_angle != previous_angle:
			asteroid_destroyed_in_this_sweep += 1
			total_asteroid_destroyed += 1
			target[2] = True
			grid[target[3][1]][target[3][0]] = False
			
			print('Destroyed ', total_asteroid_destroyed, ' ', target[3])
			
			previous_angle = current_angle
			
			if total_asteroid_destroyed == 200:
				answer = target[3]
			
	if asteroid_destroyed_in_this_sweep == 0:
		break
		
print(answer[0]*100 + answer[1])
	
	
