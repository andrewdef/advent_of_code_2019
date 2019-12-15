from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]
	
computer = CodeExecutor(program)
output = computer.run([1])

for x in output:
	print(x)