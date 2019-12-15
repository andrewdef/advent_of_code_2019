from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]
	
program[1] = 12
program[2] = 2

computer = CodeExecutor(program)
computer.run([])

print(computer.program[0])

		