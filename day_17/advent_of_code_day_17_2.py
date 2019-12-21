from common.intcodecomputer import CodeExecutor
import itertools

def create_grid(points):
	grid = []
	
	row = []
	for p in points:
		if p == 10:
			grid.append(row)
			row = []
		else:
			row.append(chr(p))	
	
	return grid
	
def try_move(grid, current_position, direction, current_orientation):
	new_position = [current_position[0], current_position[1]]
	new_orientation = None
	rotation = None
	
	rotation_map = { 0 : 'L'
					,1 : 'N'
					,2 : 'R'
				   }
	
	direction_map = { ('UP', 'L') : 'LEFT'
					 ,('UP', 'N') : 'UP'
					 ,('UP', 'R') : 'RIGHT'
					 ,('RIGHT', 'L') : 'UP'
					 ,('RIGHT', 'N') : 'RIGHT'
					 ,('RIGHT', 'R') : 'DOWN'
					 ,('DOWN', 'L') : 'RIGHT'
					 ,('DOWN', 'N') : 'DOWN'
					 ,('DOWN', 'R') : 'LEFT'
					 ,('LEFT', 'L') : 'DOWN'
					 ,('LEFT', 'N') : 'LEFT'
					 ,('LEFT', 'R') : 'UP'
					}
					
	rotation = rotation_map[direction]
	new_orientation = direction_map[(current_orientation, rotation)]
	
	if current_orientation == 'UP':
		if direction == 0:
			new_position[0] -= 1
		elif direction == 1:
			new_position[1] -= 1
		elif direction == 2:
			new_position[0] += 1
	elif current_orientation == 'RIGHT':
		if direction == 0:
			new_position[1] -= 1
		elif direction == 1:
			new_position[0] += 1
		elif direction == 2:
			new_position[1] += 1
	elif current_orientation == 'DOWN':
		if direction == 0:
			new_position[0] += 1
		elif direction == 1:
			new_position[1] += 1
		elif direction == 2:
			new_position[0] -= 1
	elif current_orientation == 'LEFT':
		if direction == 0:
			new_position[1] += 1
		elif direction == 1:
			new_position[0] -= 1
		elif direction == 2:
			new_position[1] -= 1
		
	if new_position[1] < 0 or new_position[1] >= len(grid) or new_position[0] < 0 or new_position[0] >= len(grid[new_position[1]]):
		return (None, None, None)

	object = grid[new_position[1]][new_position[0]]
	if object == '#':
		return (new_position, rotation, new_orientation)
	else:
		return (None, None, None)

def is_same_point(a, b):
	return (a[0] == b[0] and a[1] == b[1])

def has_already_visited(visited_intersections, current_position, new_position):
	all_visited_points = visited_intersections.get(tuple(current_position))
	
	if all_visited_points == None:
		return False
	else:
		return ( tuple(new_position) in all_visited_points )

def get_tiles_of_scaffolding(grid):
	all_tiles = set()
	
	for y, row in enumerate(grid):
		for x, t in enumerate(row):
			if t == '#':
				all_tiles.add((x, y))
	
	return all_tiles

def add_point_to_visited_intersections(visited_intersections, intersection_center, p, p_minus_1, num_of_possible_routes):
	visited_intersections_copy = {}
	for center in visited_intersections:
		visited_intersections_copy[center] = visited_intersections[center].copy()
		
	if num_of_possible_routes > 1 :
		intersection_center = tuple(intersection_center)
		if intersection_center in visited_intersections_copy:
			visited_intersections_copy[intersection_center].append(tuple(p))
			visited_intersections_copy[intersection_center].append(tuple(p_minus_1))
		else:
			visited_intersections_copy[intersection_center] = [tuple(p)]
			visited_intersections_copy[intersection_center].append(tuple(p_minus_1))

	return visited_intersections_copy

def walk_scaffold(grid, start_point):
	solutions = []
	all_tiles_of_scaffolding = get_tiles_of_scaffolding(grid)

	iteration = 0
	
	current_states = [([], start_point, 'UP', all_tiles_of_scaffolding, {}, None)]
	while( len(current_states) != 0 ):
		new_states = []
		iteration += 1
		#print('Iteration: ', iteration)

		for state in current_states:
			path = state[0]
			current_position = state[1]
			current_orientation = state[2]
			tiles_not_visited = state[3]
			visited_intersections = state[4]
			previous_position = state[5]
			
			if len(tiles_not_visited) == 0:
				solutions.append(path)
				continue

			possible_routes = []
			for direction in range(3):
				route = try_move(grid, current_position, direction, current_orientation)
				if route[0] != None:
					possible_routes.append(route)
			
			for (new_position, rotation, new_orientation) in possible_routes:
				if not has_already_visited(visited_intersections, current_position, new_position):
					path_copy = path.copy()
					
					if rotation in ('R', 'L'):
						path_copy.append(rotation)
						path_copy.append(1)
					else:
						path_copy[-1] += 1
					
					tiles_not_visited_copy = tiles_not_visited.copy()
					tiles_not_visited_copy.discard(tuple(new_position))
					
					visited_intersections_copy = add_point_to_visited_intersections(visited_intersections, current_position, new_position, previous_position, len(possible_routes))
					
					#print(path_copy, new_position, new_orientation, len(tiles_not_visited_copy), visited_intersections_copy)
					#input('continue')
					
					new_state = (path_copy, new_position, new_orientation, tiles_not_visited_copy, visited_intersections_copy, current_position)
					new_states.append(new_state)
		
		current_states = new_states
		
	shorter_solution = None
	for solution in solutions:
		if shorter_solution == None or len(solution) < len(shorter_solution):
			shorter_solution = solution
			
	return shorter_solution	

def find_start_pos(grid):
	for y, row in enumerate(grid):
		for x, t in enumerate(row):
			if t == '^' :
				return [x, y]

def load_grid_from_file(input_file):
	grid = []
	with open(input_file) as fd:
		for line in fd.read().split('\n'):
			grid.append([x for x in line])
			
	return grid

def sequence_matches_at(index, sequence, path):
	for i, x in enumerate(sequence):
		if (index + i) >= len(path):
			return False
		elif path[index + i] != x:
			return False
		
	return True
	
def find_repeating_sequences(path):
	matched_sequences = {}
	sequence_length = 2

	while( True ):
		sequence_length += 2
		matched_sequences[sequence_length] = []
		
		for i in range(0, len(path) - sequence_length, 2):
			sequence = tuple(path[i:i + sequence_length])
			
			if sequence in matched_sequences[sequence_length]:
				continue
			
			k = 0
			number_of_matches = 0
			while( k < len(path) ):
				if sequence_matches_at(k, sequence, path):
					number_of_matches += 1
					k += len(sequence)
				else:
					k += 1
					
			if number_of_matches > 1:
				matched_sequences[sequence_length].append(sequence)
		
		if len(matched_sequences[sequence_length]) == 0:
			break
		
	return [match for all_matches in matched_sequences.values() for match in all_matches]

def replace_all(path, sequence_to_replace, replacement):
	replaced_path = []
	
	k = 0
	while( k < len(path) ):
		if sequence_matches_at(k, sequence_to_replace, path):
			replaced_path.append(replacement)
			k += len(sequence_to_replace)
		else:
			replaced_path.append(path[k])
			k += 1
			
	return replaced_path
	
def compress_path(path):
	path_only_strings = [str(x) for x in path]
	sequences = find_repeating_sequences(path_only_strings)
	
	for permutation in itertools.permutations(sequences, 3):
		compressed_path = replace_all(path_only_strings, permutation[0], 'A')
		compressed_path = replace_all(compressed_path, permutation[1], 'B')
		compressed_path = replace_all(compressed_path, permutation[2], 'C')
		
		if 'R' not in compressed_path and 'L' not in compressed_path:
			return (','.join(compressed_path), ','.join(permutation[0]), ','.join(permutation[1]), ','.join(permutation[2]))			
			
	return (None, None, None, None)		
		
program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

robot = CodeExecutor(program)
grid = create_grid(robot.run([]))
	
path = walk_scaffold(grid, find_start_pos(grid))
print(path)

(main_routine, routine_a, routine_b, routine_c) = compress_path(path)
print(main_routine)
print(routine_a)
print(routine_b)
print(routine_c)

program[0] = 2
robot = CodeExecutor(program)

robot.run([])
robot.print_output_as_ascii()

robot.run(main_routine)
robot.print_output_as_ascii()

robot.run(routine_a)
robot.print_output_as_ascii()

robot.run(routine_b)
robot.print_output_as_ascii()

robot.run(routine_c)
robot.print_output_as_ascii()

robot.run('n')
robot.print_output_as_ascii()