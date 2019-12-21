from pathlib import Path
import datetime

class Map:
	def __init__(self):
		self.grid = []
		self.keys = {}
		self.doors = {}
		self.paths_between_keys = {}
		self.starting_points = []
		self.input_file = ''
		
	def init_from_file(self, input_file):
		self.grid = []
	
		with open(input_file) as fd:
			i = 0
			
			for line in fd.readlines():
				row = []
				j = 0
				
				for object in line:
					if object == '\n':
						continue

					row.append(object)
					
					object_type = self.get_object_type(object)
					
					if object_type == 'DOOR':
						self.doors[object] = [j, i]
					elif object_type == 'KEY':
						self.keys[object] = [j, i]
			
					j += 1
			
				self.grid.append(row)
				i += 1
		
		self.input_file = input_file

		self.find_starting_points()
		self.find_and_store_paths_btw_keys()
	
	def find_and_store_paths_btw_keys(self):
		savefile_name = 'path_btw_keys' + '-' + self.input_file
		
		savefile = Path(savefile_name)
		if savefile.is_file():
			self.load_paths_from_file(savefile_name)
			return
		
		all_keys = [x for x in self.keys.keys()]
		
		for starting_point in self.starting_points:
			point_symbol = self.grid[starting_point[1]][starting_point[0]]
			
			for key_id in all_keys:
				mapping_key = point_symbol + '-' + key_id
				reverse_mapping_key = key_id + '-' + point_symbol
				
				solution = self.find_shortest_path([x for x in starting_point], self.keys[key_id])		
				if solution == None:
					continue
					
				path = solution[0]
				doors = solution[1]
				
				self.paths_between_keys[mapping_key] = [path, doors]
				self.paths_between_keys[reverse_mapping_key] = [path[-1::-1], doors]
			
		for i in range(0, len(all_keys) - 1):
			starting_key = all_keys[i]
			
			for j in range(i + 1, len(all_keys)):
				destination_key = all_keys[j]
				
				mapping_key = starting_key + '-' + destination_key
				reverse_mapping_key = destination_key + '-' + starting_key

				solution = self.find_shortest_path(self.keys[starting_key], self.keys[destination_key])
				if solution == None:
					continue

				path = solution[0]
				doors = solution[1]
				
				self.paths_between_keys[mapping_key] = [path, doors]
				self.paths_between_keys[reverse_mapping_key] = [path[-1::-1], doors]
				
		self.save_paths_in_file(savefile_name)
		
	def save_paths_in_file(self, dest_file):
		with open(dest_file, 'w') as fd:
			for path_id in self.paths_between_keys:
				fd.write(path_id + ':' + '#'.join([str(x[0]) + ',' + str(x[1]) for x in self.paths_between_keys[path_id][0]]) 
							+ '|' + '-'.join([str(x) for x in self.paths_between_keys[path_id][1]])
							+ '\n')
	
	def load_paths_from_file(self, input_file):
		with open(input_file, 'r') as fd:
			for line in fd.read().split('\n'):
				if line == '':
					continue

				key = line.split(':')[0]
				values = line.split(':')[1].split('|')
				
				path = []
				for p in values[0].split('#'):
					x = int(p.split(',')[0])
					y = int(p.split(',')[1])
					path.append([x, y])
					
				doors = []
				for door in values[1].split('-'):
					if door != '':
						doors.append(door)

				self.paths_between_keys[key] = [path, doors]				

	def is_same_point(self, a, b):
		return (a[0] == b[0] and a[1] == b[1])

	def get_object_type(self, object):
		num = ord(object)
		if ( num <= 122 and num >= 97 ):
			return 'KEY'
		elif ( num <= 90 and num >= 65 ):
			return 'DOOR'
		elif num == 35:
			return 'WALL'
		elif num == 64:
			return 'STARTING_POINT'
		else:
			return 'EMPTY'

	def is_opposite_direction(self, direction_1, direction_2):
		if direction_1 == 1 and direction_2 == 2:
			return True
		elif direction_1 == 2 and direction_2 == 1:
			return True
		elif direction_1 == 3 and direction_2 == 4:
			return True
		elif direction_1 == 4 and direction_2 == 3:
			return True
			
		return False
		
	def find_object_at(self, p):
		object_type = self.get_object_type(self.grid[p[1]][p[0]])
		
		if object_type == 'DOOR' and self.doors.get(self.grid[p[1]][p[0]]) == None:
			object_type = 'EMPTY'

		return object_type
		
	def try_move(self, current_position, direction, ignore_doors):
		new_position = [current_position[0], current_position[1]]
		
		if direction == 1:
			new_position[1] -= 1
		elif direction == 2:
			new_position[1] += 1
		elif direction == 3:
			new_position[0] -= 1
		elif direction == 4:
			new_position[0] += 1
			
		if new_position[0] < 0 or new_position[0] >= len(self.grid[0]) or new_position[1] < 0 or new_position[1] >= len(self.grid):
			return None
		
		object_type = self.find_object_at(new_position)
		if object_type == 'WALL':
			return None
		elif object_type == 'DOOR' and not ignore_doors:
			return None	
		else:
			return new_position

	def find_shortest_path(self, start_point, end_point):
		solutions = []
		passed_points = []

		current_states = [([], start_point, None, [])]
		while( len(current_states) != 0 ):
			new_states = []
			
			for state in current_states:
				path = state[0]
				current_position = state[1]
				coming_from = state[2]
				doors_in_between = state[3]
				
				doors_in_between_copy = doors_in_between.copy()
				object_at_position = self.find_object_at(current_position)
				if object_at_position == 'DOOR':
					doors_in_between_copy.append(self.grid[current_position[1]][current_position[0]])
					
				path_copy = path.copy()
				path_copy.append(current_position)				
				
				if self.is_same_point(current_position, end_point):
					solutions.append([path_copy, doors_in_between_copy])
					continue

				for direction in range(1, 5):
					if self.is_opposite_direction(direction, coming_from):
						continue
					
					new_position = self.try_move(current_position, direction, True)

					if new_position != None and not self.has_already_visited(passed_points, new_position):
						passed_points.append(new_position)

						new_state = (path_copy, new_position, direction, doors_in_between_copy)
						new_states.append(new_state)
			
			current_states = new_states

		shorter_solution = None
		for solution in solutions:
			if shorter_solution == None or len(solution[0]) < len(shorter_solution[0]):
				shorter_solution = solution
				
		return shorter_solution
			
	def has_already_visited(self, path, new_position):
		for p in path:
			if self.is_same_point(p, new_position):
				return True
			
		return False

	def find_next_available_keys(self, keys_collected, current_position):
		#print(self.current_position)
		found_keys = {}
		
		object_in_current_position = self.grid[current_position[1]][current_position[0]]
	
		for key_id in self.keys:
			if key_id in keys_collected:
				continue
				
			mapping_key = object_in_current_position + '-' + key_id
			path = self.paths_between_keys.get(mapping_key)
			
			if path == None:
				continue
			
			if all(door_id.lower() in keys_collected for door_id in path[1]):
				found_keys[key_id] = path[0]

		return found_keys
		
	def print_map(self):
		print('Map for bot ', self.id)
		
		for row in self.grid:
			print(''.join(row))
	
	def find_starting_points(self):
		starting_points = []
		k = 0
		
		for i in range(len(self.grid)):
			row = self.grid[i]
			
			for j in range(len(row)):
				if row[j] == '@':
					k = k + 1
					
					starting_points.append((j, i))
					self.grid[i][j] = str(k)
					
		self.starting_points = starting_points
	
	def collect_all_keys(self, start_points):
		shortest_solution = 1e10

		current_states = { (frozenset(), tuple(start_points)) : 0 }

		while( len(current_states) != 0 ):
			new_states = {}
			
			for (collected_keys, current_positions), traveled_distance in current_states.items():
				if len(collected_keys) == len(self.keys):
					shortest_solution = min(shortest_solution, traveled_distance)
					continue
				
				for index, current_position in enumerate(current_positions):
					current_position = [x for x in current_position]
					next_paths = self.find_next_available_keys(collected_keys, current_position)

					for key_id in next_paths:
						current_positions_copy = [x for x in current_positions]
						
						next_path = next_paths[key_id]
						
						collected_keys_copy = collected_keys.union(frozenset(key_id))
						new_traveled_distance = traveled_distance + (len(next_path) - 1)
						
						current_positions_copy[index] = tuple(next_path[-1])
						new_state = (collected_keys_copy, tuple(current_positions_copy))
						
						existing_distance = new_states.get(new_state, 1e10)
						new_states[new_state] = min(existing_distance, new_traveled_distance)
			
			current_states = new_states
			
		return shortest_solution