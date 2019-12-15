from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

game = CodeExecutor(program)
tiles = []

while( game.is_halted != True ):
	input = []
	tiles = game.run(input)
	
block_tiles = 0
i = 2

while( True ):	
	if i >= len(tiles):
		break
		
	tile_type = tiles[i]
	
	if tile_type == 2:
		block_tiles += 1
	i += 3
	
print(block_tiles)

		

