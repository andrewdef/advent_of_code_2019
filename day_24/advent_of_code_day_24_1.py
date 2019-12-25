def layout_has_repeated(grid_state, saved_states):
	for saved_state in saved_states:
		if grid_state == saved_state:
			return True
			
	return False
	
def find_adiacent_bugs(x, y, grid):
	deltas = [[0, 1], [0, -1], [1, 0], [-1, 0]]
	
	adiacent_bugs = 0
	for delta_x, delta_y in deltas:
		new_x = x + delta_x
		new_y = y + delta_y
		
		if new_y >= 0 and new_y < len(grid) and new_x >= 0 and new_x < len(grid[new_y]) and grid[new_y][new_x] == '#':
			adiacent_bugs += 1
			
	return adiacent_bugs	
	
def evolve_grid(grid):
	new_grid = []
	for row in grid:
		new_grid.append(row.copy())
	
	for y, row in enumerate(grid):
		for x, t in enumerate(row):
			num_adiacent_bugs = find_adiacent_bugs(x, y, grid)

			if t == '#' and num_adiacent_bugs != 1:
				new_grid[y][x] = '.'
			elif t == '.' and num_adiacent_bugs in (1, 2):
				new_grid[y][x] = '#'

	return new_grid
	
def calculate_biodiversity_rating(grid):
	exponent = 0
	biodiversity_rating = 0
	
	for row in grid:
		for x in row:
			if x == '#':
				biodiversity_rating += pow(2, exponent)
				
			exponent += 1

	return biodiversity_rating

def print_grid(grid):
	for row in grid:
		print(''.join(row))

def run():
	grid = []
	with open('input.txt') as fd:
		for line in fd.read().split('\n'):
			grid.append([x for x in line])
			
	saved_states = []
	iteration = 0
	while( True ):
		grid = evolve_grid(grid)

		if layout_has_repeated(grid, saved_states):
			print(calculate_biodiversity_rating(grid))
			print_grid(grid)
			break
			
		saved_states.append(grid.copy())
	
run()