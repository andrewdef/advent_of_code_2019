from common.intcodecomputer import CodeExecutor

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
	
def calculate_alignment_parameter(grid):
	alignment_parameter = 0
	
	for y in range(1, len(grid) - 2):
		row = grid[y]
		
		for x in range(1, len(row) - 1):
			object = row[x]
			
			if object == '#' and grid[y - 1][x] == '#' and grid[y + 1][x] and grid[y][x + 1] == '#' and grid[y][x - 1] == '#':
				alignment_parameter += (x * y)
	
	return alignment_parameter
	
program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

robot = CodeExecutor(program)
grid = create_grid(robot.run([]))

for row in grid:
	print(''.join(row))

print(calculate_alignment_parameter(grid))
