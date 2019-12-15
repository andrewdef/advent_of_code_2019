from common.intcodecomputer import CodeExecutor

def execute_program(initial_state, noun, verb):
	program = [x for x in initial_state]
	
	program[1] = noun
	program[2] = verb
	
	computer = CodeExecutor(program, memory_amount=1000)
	computer.run([])
	
	return computer.program[0]

initial_state = []
with open('input.txt') as fd:
	initial_state = [int(x) for x in fd.read().split(',')]
	
for noun in range(0, 99):
	for verb in range(0, 99):
	
		result = execute_program(initial_state, noun, verb)
	
		if result == 19690720:
			print("Result: " + str((100 * noun + verb)))
			break

		