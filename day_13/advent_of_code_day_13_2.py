from common.intcodecomputer import CodeExecutor

def render_screen(tiles, entity_positions):
	score = None
	
	tile_render_map = {}
	tile_render_map[0] = '.'
	tile_render_map[1] = 'X'
	tile_render_map[2] = 'b'
	tile_render_map[3] = '_'
	tile_render_map[4] = 'O'
	
	for i in range(0, len(tiles), 3):
		x = tiles[i]
		y = tiles[i + 1]
		tile_type = tiles[i + 2]
		
		if x == -1 and y == 0:
			score = tile_type
		else:
			screen[y][x] = tile_render_map[tile_type]
			
		if tile_type == 4:
			entity_positions['ball'].append(x)
		elif tile_type == 3:
			entity_positions['paddle'] = x
			
	for line in screen:
		print(''.join(line))
		
	if score != None:
		print('Score: ', score)
	
def calculate_paddle_move(ball_x_positions, paddle_position):
	if len(ball_x_positions) < 2:
		return 0
		
	ball_x = ball_x_positions[-1]
	ball_x_prev = ball_x_positions[-2]
	
	next_ball_x = ball_x + (ball_x - ball_x_prev)
	
	if next_ball_x == paddle_position:
		return 0
	elif next_ball_x < paddle_position:
		return -1
	else:
		return 1

def get_user_paddle_movement():
	joystick_position = None
	while( joystick_position == None ):
		joystick_position = input('Joystick:')
		
		if joystick_position == '':
			joystick_position = 0
		elif joystick_position in ('2'):
			joystick_position = 1
		elif joystick_position in ('1'):
			joystick_position = -1		
		else:
			joystick_position = None
	return joystick_position

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

program[0] = 2
game = CodeExecutor(program)

SCREEN_SIZE_X = 35
SCREEN_SIZE_Y = 23
screen = [['.' for j in range(0, SCREEN_SIZE_X)] for i in range(0, SCREEN_SIZE_Y)]

reload = input('Reload saved state?: ')
if reload.lower() in ('yes', ''):
	with open('save0', 'r') as fd:
		savestate = [int(x) for x in fd.read().split(',')]
		
	game_input = [x for x in savestate]
else:
	game_input = []
	savestate = []
	
entity_positions = {}
entity_positions['ball'] = []
entity_positions['paddle'] = None

while( game.is_halted != True ):
	tiles = game.run(game_input)
	render_screen(tiles, entity_positions)
	
	joystick_position = calculate_paddle_move(entity_positions['ball'], entity_positions['paddle'])
	game_input = [joystick_position]
	
	savestate.append(joystick_position)
	
with open('save0', 'w') as fd:
	fd.write(','.join([str(x) for x in savestate]))
