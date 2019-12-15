from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

executor = CodeExecutor(program)
output = executor.run([1])
print(output)