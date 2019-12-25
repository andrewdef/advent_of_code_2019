def classify_point(x, y, grid):
	if x == 0 and y == 0:
		point_category = 'UP_LEFT_OUTER_CORNER'
	elif x == 0 and y == (len(grid) - 1):
		point_category = 'DOWN_LEFT_OUTER_CORNER'
	elif x == (len(grid[y]) - 1) and y == 0:
		point_category = 'UP_RIGHT_OUTER_CORNER'
	elif x == (len(grid[y]) - 1) and y == (len(grid) - 1):
		point_category = 'DOWN_RIGHT_OUTER_CORNER'
	elif x == 0:
		point_category = 'LEFT_OUTER_EDGE'
	elif x == (len(grid[y]) - 1):
		point_category = 'RIGHT_OUTER_EDGE'
	elif y == 0:
		point_category = 'UP_OUTER_EDGE'
	elif y == (len(grid) - 1):
		point_category = 'DOWN_OUTER_EDGE'
	elif x == 2 and y == 1:
		point_category = 'UP_INNER_EDGE'
	elif x == 2 and y == 3:
		point_category = 'DOWN_INNER_EDGE'
	elif y == 2 and x == 1:
		point_category = 'LEFT_INNER_EDGE'
	elif y == 2 and x == 3:
		point_category = 'RIGHT_INNER_EDGE'
	else:
		point_category = 'INTERNAL'
		
	return point_category
		
def find_adiacent_bugs(x, y, level, grids):
	all_deltas ={
				 'INTERNAL' : [[0, 1, 0], [0, -1, 0], [1, 0, 0], [-1, 0, 0]]				 
				,'UP_OUTER_EDGE' : [[0, 1, 0], [2, 1, -1], [1, 0, 0], [-1, 0, 0]]
				,'DOWN_OUTER_EDGE' : [[2, 3, -1], [0, -1, 0], [1, 0, 0], [-1, 0, 0]]
				,'RIGHT_OUTER_EDGE' : [[0, 1, 0], [0, -1, 0], [3, 2, -1], [-1, 0, 0]]
				,'LEFT_OUTER_EDGE' : [[0, 1, 0], [0, -1, 0], [1, 0, 0], [1, 2, -1]]
				
				,'UP_LEFT_OUTER_CORNER' : [[0, 1, 0], [2, 1, -1], [1, 0, 0], [1, 2, -1]]
				,'UP_RIGHT_OUTER_CORNER' : [[2, 1, -1], [0, 1, 0], [3, 2, -1], [-1, 0, 0]]
				,'DOWN_LEFT_OUTER_CORNER' : [[2, 3, -1], [0, -1, 0], [1, 2, -1], [1, 0, 0]]
				,'DOWN_RIGHT_OUTER_CORNER' : [[2, 3, -1], [0, -1, 0], [-1, 0, 0], [3, 2, -1]]
				
				,'UP_INNER_EDGE' : [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1], [0, -1, 0], [1, 0, 0], [-1, 0, 0]]	
				,'DOWN_INNER_EDGE' : [[0, 1, 0], [0, 4, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1], [1, 0, 0], [-1, 0, 0]]
				,'RIGHT_INNER_EDGE' : [[0, 1, 0], [0, -1, 0], [1, 0, 0], [4, 0, 1], [4, 1, 1], [4, 2, 1], [4, 3, 1], [4, 4, 1]]
				,'LEFT_INNER_EDGE' : [[0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1], [0, 4, 1], [-1, 0, 0]]	
				}
	
	deltas = all_deltas[classify_point(x, y, grids[0])]
	
	adiacent_bugs = 0
	for delta_x, delta_y, delta_level in deltas:
		if delta_level == 0:
			new_x = x + delta_x
			new_y = y + delta_y
			new_level = level
		else:
			new_x = delta_x
			new_y = delta_y
			new_level = level + delta_level
		
		grid = grids.get(new_level)
		if grid == None:
			continue
		
		if new_y >= 0 and new_y < len(grid) and new_x >= 0 and new_x < len(grid[new_y]) and grid[new_y][new_x] == '#':
			adiacent_bugs += 1
			
	return adiacent_bugs	

def add_empty_grid(grids, level, width, height):
	grid_to_add = []
	
	for i in range(height):
		grid_to_add.append(['.'] * width)
	
	grids[level] = grid_to_add
	
def has_bugs_in_inner_edge(grid):
	for x in range(1, 4):
		if grid[1][x] == '#':
			return True

	for x in (1, 3):
		if grid[2][x] == '#':
			return True
			
	for x in range(1, 4):
		if grid[3][x] == '#':
			return True
			
	return False
	
def has_bugs_in_outer_edge(grid):
	for x in range(0, 5):
		if grid[0][x] == '#':
			return True
			
	for y in range(1, 4):
		if grid[y][0] == '#':
			return True

	for y in range(1, 4):
		if grid[y][4] == '#':
			return True
			
	for x in range(1, 4):
		if grid[3][x] == '#':
			return True
			
	return False
	
def evolve_grids(grids):
	updates = []
	
	index = sorted(grids)[-1]
	most_upward_grid = grids[index]
	if has_bugs_in_outer_edge(most_upward_grid):
		add_empty_grid(grids, index + 1, 5, 5)
		
	index = sorted(grids)[0]
	most_inward_grid = grids[index]
	if has_bugs_in_inner_edge(most_inward_grid):
		add_empty_grid(grids, index - 1, 5, 5)		
	
	for level in grids:
		grid = grids[level]
		
		for y, row in enumerate(grid):
			for x, t in enumerate(row):
				if x == 2 and y == 2:
					continue

				num_adiacent_bugs = find_adiacent_bugs(x, y, level, grids)

				if t == '#' and num_adiacent_bugs != 1:
					updates.append((level, x, y, '.'))
				elif t == '.' and num_adiacent_bugs in (1, 2):
					updates.append((level, x, y, '#'))

	for level, x, y, t in updates:
		grids[level][y][x] = t
	
def count_all_bugs(grids):
	all_bugs = 0
	for level in grids:
		grid = grids[level]

		for row in grid:
			for t in row:
				if t == '#':
					all_bugs += 1
					
	return all_bugs

def print_grid(grids):
	for level in sorted(grids):

		grid = grids[level]
		print(f"Depth: {level}")

		for row in grid:
			print(''.join(row))

def run():
	grids = {}
	with open('input.txt') as fd:
		grid = []
		for line in fd.read().split('\n'):
			grid.append([x for x in line])
			
		grids[0] = grid
			
	iteration = 0
	while( True ):
		grid = evolve_grids(grids)
		iteration += 1
		
		if iteration == 200:
			print(count_all_bugs(grids))
			print_grid(grids)
			break
	
run()