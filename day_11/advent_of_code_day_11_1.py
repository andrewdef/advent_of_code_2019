import itertools

class CodeExecutor:
	program = []
	instruction_pointer = 0
	relative_memory_pointer = 0
	is_halted = False
	is_initialized = False
	is_waiting_for_input = False
	current_direction = 1
	current_position = [2, 2]
	
	def __init__(self, amplifier_code):
		self.program = amplifier_code.copy()
		
		for i in range(0, 2000000):
			self.program.append(0)

		self.instruction_pointer = 0
		self.is_halted = False
		self.is_initialized = False
		self.is_waiting_for_input = False
		self.current_direction = 1
		self.current_position = [2, 2]
		
	def fetch_parameter_value(self, instruction_pointer, parameter_index, parameter_modes, program, parameter_mode=None):
		if parameter_mode == None:
			parameter_mode = 0
			if parameter_index < len(parameter_modes):
				parameter_mode = parameter_modes[parameter_index]
				
		parameter_value = program[instruction_pointer + 1 + parameter_index]
		
		if parameter_mode == 2:
			return program[self.relative_memory_pointer + parameter_value]
		elif parameter_mode == 0:
			return program[parameter_value]
		else:
			return parameter_value
			
	def fetch_address_of_result(self, instruction_pointer, parameter_index, parameter_modes, program):
		parameter_mode = 1
		if parameter_index < len(parameter_modes):
			parameter_mode = parameter_modes[parameter_index]
				
		parameter_value = program[instruction_pointer + 1 + parameter_index]
		
		if parameter_mode == 2:
			return self.relative_memory_pointer + parameter_value
		elif parameter_mode == 1:
			return parameter_value

	def run(self, inputs):
		input_pointer = 0
		output_pointer = 0
		output = []
		
		if not self.is_initialized:
			self.is_initialized = True

		while( True ):
			opcode = str(self.program[self.instruction_pointer])

			if len(opcode) > 1:
				parameter_modes = [int(x) for x in opcode[-3::-1]]
				opcode = int(opcode[-2:])
			else:
				opcode = int(opcode)
				parameter_modes = []
			
			if opcode == 99:
				self.is_halted = True
				break
			
			if opcode == 1:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
				
				self.program[address_of_result] = operand_1 + operand_2
				
				opcode_signature_size = 4
			elif opcode == 2:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
				
				self.program[address_of_result] = operand_1 * operand_2
				
				opcode_signature_size = 4
			elif opcode == 3:
				address_of_result = self.fetch_address_of_result(self.instruction_pointer, 0, parameter_modes, self.program)
				
				if input_pointer >= len(inputs):
					self.is_waiting_for_input = True
					break
				else:
					self.is_waiting_for_input = False
					
				self.program[address_of_result] = inputs[input_pointer]
				
				input_pointer += 1
				opcode_signature_size = 2
			elif opcode == 4:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				output.append(operand_1)
				
				opcode_signature_size = 2
			elif opcode == 5:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				
				if operand_1 != 0:
					self.instruction_pointer = operand_2
					opcode_signature_size = 0
				else:
					opcode_signature_size = 3
			elif opcode == 6:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				
				if operand_1 == 0:
					self.instruction_pointer = operand_2
					opcode_signature_size = 0
				else:
					opcode_signature_size = 3
			elif opcode == 7:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
				
				if operand_1 < operand_2:
					self.program[address_of_result] = 1
				else:
					self.program[address_of_result] = 0
					
				opcode_signature_size = 4
			elif opcode == 8:
				operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
				address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
				
				if operand_1 == operand_2:
					self.program[address_of_result] = 1
				else:
					self.program[address_of_result] = 0
					
				opcode_signature_size = 4
			elif opcode == 9:
				offset = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
				
				self.relative_memory_pointer += offset
				opcode_signature_size = 2
			else:
				raise ValueError("Unknown opcode: " + opcode)
			
			self.instruction_pointer += opcode_signature_size
			
		return output

	def paint(self, point, color):
		grid[point[1]][point[0]][0] = color
		grid[point[1]][point[0]][1] = True

	def get_current_panel_color(self, point):
		print(point)
		return (grid[point[1]][point[0]][0])
		
	def turn_and_move(self, turn_direction):
		UP = 1
		RIGHT = 2
		DOWN = 3
		LEFT = 4

		if turn_direction == 0:
			self.current_direction -= 1
		else:
			self.current_direction += 1
			
		if self.current_direction == 0:
			self.current_direction = LEFT
		elif self.current_direction == 5:
			self.current_direction = UP
			
		if self.current_direction == UP:
			self.current_position[1] += 1
		elif self.current_direction == DOWN:
			self.current_position[1] -= 1
		elif self.current_direction == RIGHT:
			self.current_position[0] += 1
		elif self.current_direction == LEFT:
			self.current_position[0] -= 1

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

grid = []
for i in range(0, 100):
	grid.append([[0, False] for k in range(0, 100)])
	
STARTING_POSITON = [50, 50]

BLACK = 0
WHITE = 1

robot = CodeExecutor(program)
robot.current_position = STARTING_POSITON.copy()
robot.current_direction = 1

while( robot.is_halted != True ):
	input = [robot.get_current_panel_color(robot.current_position)]
	output = robot.run(input)
	
	robot.paint(robot.current_position, output[0])
	robot.turn_and_move(output[1])
	
painted_panels = 0
for row in grid:
	for p in row:
		if p[1] == True:
			painted_panels += 1
			
print(painted_panels)
