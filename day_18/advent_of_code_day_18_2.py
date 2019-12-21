from map import Map
			
def print_map(map):
	grid = map.grid.copy()
	
	for row in grid:
		print(''.join(row))

def print_path(map, path):
	grid = map.grid.copy()
	
	for p in path:
		grid[p[1]][p[0]] = '+';
	
	for row in grid:
		print(''.join(row))
		
def run():
	map = Map()
	map.init_from_file('input2.txt')

	print(map.collect_all_keys(map.starting_points))
run()