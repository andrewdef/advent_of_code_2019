import itertools

from common.intcodecomputer import CodeExecutor

def amplify_signal(num_amplifiers, input_signal, amplifier_code, phase_sequence):
	current_input_signal = input_signal
	
	for i in range(0, num_amplifiers):
		program_input = [phase_sequence[i], current_input_signal]
		
		amplifier = CodeExecutor(amplifier_code, memory_amount=2000)
		output_signal = amplifier.run(program_input)
		
		current_input_signal = output_signal[0]
		
	return current_input_signal

NUMBER_OF_AMPLIFIERS = 5

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

all_phase_combinations = itertools.permutations(range(5), 5)

max_signal_output = -1
best_sequence = None
for phase_sequence in all_phase_combinations:
	signal_output = amplify_signal(NUMBER_OF_AMPLIFIERS, 0, program, phase_sequence)
	
	if signal_output > max_signal_output:
		best_sequence = phase_sequence
		max_signal_output = signal_output
		
print(max_signal_output)
print(best_sequence)