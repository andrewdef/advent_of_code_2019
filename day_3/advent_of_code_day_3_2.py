def calculate_manhattan_distance(p, q):
	return (abs(p[0] - q[0]) + abs(p[1] - q[1]))
	
def traverse_path(path):
	points = {}
	current_x = 0
	current_y = 0
	steps = 0
	
	for move in path:
		direction = move[0]
		distance = int(move[1:])
		
		for i in range(0, distance):
			if direction == 'U':
				current_y += 1
			elif direction == 'D':
				current_y -= 1
			elif direction == 'L':
				current_x -= 1
			elif direction == 'R':
				current_x += 1
			else:
				raise ValueError('Unknown direction: ' + direction)
			
			steps += 1
			
			if points.get(current_x) == None:
				points[current_x] = {}
				
			if points.get(current_x).get(current_y) == None:
				points[current_x][current_y] = steps
	
	return points

with open('input.txt') as fd:
	path_1 = fd.readline().split(',')
	path_2 = fd.readline().split(',')

points_1 = traverse_path(path_1)
points_2 = traverse_path(path_2)

min_distance = -1
for x in points_1:
	for y in points_1[x]:
		all_y = points_2.get(x)
		
		if all_y != None:
			for y2 in all_y:
				if y2 == y:
					steps_1 = points_1[x][y]
					steps_2 = points_2[x][y]
					total_steps = steps_1 + steps_2
					
					if total_steps < min_distance or min_distance == -1:
						min_distance = total_steps
			
print(min_distance)
		