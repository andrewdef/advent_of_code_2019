from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

points_affected = 0

for x in range(50):
	for y in range(50):
	
		drone = CodeExecutor(program, memory_amount=200)
		points_affected += drone.run([x, y])[0]
	
print(points_affected)

