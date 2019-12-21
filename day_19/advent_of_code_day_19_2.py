from common.intcodecomputer import CodeExecutor

def print_grid(grid):
	render_map = { 0 : '.'
				  ,1 : '#'
				  ,2 : 'O'
				 }
				 
	for row in grid:
		print(''.join([render_map[x] for x in row]))

def find_edge_for_square(size, draw_grid=True):
	start_x = 12 + ((size - 2) * 10) - size
	start_y = 6 + ((size - 2) * 5) - size

	for y in range(start_y, start_y + 100):
		row = []
		
		for x in range(start_x, start_x + 100):	
		
			drone = CodeExecutor(program, memory_amount=200)
			out1 = drone.run([x, y])[0]
			
			drone = CodeExecutor(program, memory_amount=200)
			out2 = drone.run([x + size - 1, y])[0]
			
			drone = CodeExecutor(program, memory_amount=200)
			out3 = drone.run([x, y + size - 1])[0]

			if out1 == 1 and out2 == 1 and out3 == 1:
				if draw_grid:
					for dy in range(y, y + size):
						for dx in range(x, x + size):
							grid[dy][dx] = 2
				return [x, y]
	
def scan_grid(size):
	grid = []
	for y in range(size):
		row = []
		
		for x in range(size):	
			drone = CodeExecutor(program, memory_amount=200)
			out = drone.run([x, y])[0]
			
			row.append(out)
			
		grid.append(row)
	
program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

#grid = scan_grid(50)

edge = find_edge_for_square(100, False)
print(edge)
print(edge[0] * 10000 + edge[1])
#print_grid(grid)