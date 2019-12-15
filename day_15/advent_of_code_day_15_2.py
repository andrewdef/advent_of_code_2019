from common.intcodecomputer import CodeExecutor

def mark_object_in_direction(object_type, current_position, direction):
	object_position = [current_position[0], current_position[1]]
	
	if direction == 1:
		object_position[1] -= 1
	elif direction == 2:
		object_position[1] += 1
	elif direction == 3:
		object_position[0] -= 1
	elif direction == 4:
		object_position[0] += 1
		
	#print(direction, object_position, object_type)
	grid[object_position[1]][object_position[0]] = object_type

def already_been_that_way(current_position, direction):
	new_position = [current_position[0], current_position[1]]
	
	if direction == 1:
		new_position[1] -= 1
	elif direction == 2:
		new_position[1] += 1
	elif direction == 3:
		new_position[0] -= 1
	elif direction == 4:
		new_position[0] += 1
		
	#print(direction, object_position, object_type)
	if grid[new_position[1]][new_position[0]] != -1:
		return True
	else:
		return False
	
def move(current_position, direction):
	new_position = [current_position[0], current_position[1]]
	
	if direction == 1:
		new_position[1] -= 1
	elif direction == 2:
		new_position[1] += 1
	elif direction == 3:
		new_position[0] -= 1
	elif direction == 4:
		new_position[0] += 1
	
	return new_position		

def is_opposite_direction(direction_1, direction_2):
	if direction_1 == 1 and direction_2 == 2:
		return True
	elif direction_1 == 2 and direction_2 == 1:
		return True
	elif direction_1 == 3 and direction_2 == 4:
		return True
	elif direction_1 == 4 and direction_2 == 3:
		return True
		
	return False

def get_opposite_direction(direction):
	opposite_direction = -1
	if direction == 1:
		opposite_direction = 2
	elif direction == 2:
		opposite_direction = 1
	elif direction == 3:
		opposite_direction = 4
	elif direction == 4:
		opposite_direction = 3
		
	return opposite_direction

def print_maze(grid):
	char_map = {}
	char_map[-1] = ' '
	char_map[0] = '#'
	char_map[1] = '.'
	char_map[2] = 'X'
	char_map[3] = 'S'
	char_map[4] = 'O'
	
	grid[START_POSITION[1]][START_POSITION[0]] = 3
	
	for row in grid:
		print(''.join([char_map[p] for p in row]))
		
def visit_maze(droid, current_position, coming_from, path, object_in_current_position):
	opposite_direction = None
	
	path.append(current_position)
	if object_in_current_position == 2:
		solutions.append(path)
	
	for direction in range(1, 5):
		if is_opposite_direction(direction, coming_from):
			opposite_direction = direction
			continue
		elif already_been_that_way(current_position, direction):
			continue

		status = droid.run([direction])[0]
		mark_object_in_direction(status, current_position, direction)

		if status in (1, 2):
			path_copy = path.copy()
			visit_maze(droid, move(current_position, direction), direction, path_copy, status)
	
	if opposite_direction != None:
		status = droid.run([opposite_direction])[0]

def find_location_of_oxygen_generator(grid):
	for y in range(0, len(grid)):
		row = grid[y]
		
		for x in range(0, len(row)):
			if row[x] == 2:
				return [x, y]

def fill_neighbors_with_oxygen(starting_point, grid):
	filled_neighbors = []
	for delta in ([0, 1], [0, -1], [1, 0], [-1, 0]):
		neighbor = [starting_point[0] + delta[0], starting_point[1] + delta[1]]
		
		if grid[neighbor[1]][neighbor[0]] in (1, 3):
			grid[neighbor[1]][neighbor[0]] = 4
			filled_neighbors.append(neighbor)	

	return filled_neighbors
		
program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

droid = CodeExecutor(program)

grid_x = 60
grid_y = 60
grid = [[-1 for i in range(0, grid_x)] for j in range(0, grid_y)]

START_POSITION = [30, 30]
solutions = []

path = []
visit_maze(droid, START_POSITION, -1, path, 3)

elapsed_minutes = 0
starting_points = [find_location_of_oxygen_generator(grid)]

while( len(starting_points) > 0 ):
	new_starting_points = []
	
	for p in starting_points:
		newly_filled_locations = fill_neighbors_with_oxygen(p, grid)
		
		for x in newly_filled_locations:
			new_starting_points.append(x)
	
	if len(new_starting_points) > 0:
		elapsed_minutes += 1
	starting_points = new_starting_points.copy()

print(elapsed_minutes)
print_maze(grid)

