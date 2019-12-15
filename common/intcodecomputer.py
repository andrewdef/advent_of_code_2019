class CodeExecutor:
	program = []
	instruction_pointer = 0
	relative_memory_pointer = 0
	is_halted = False
	is_initialized = False
	is_waiting_for_input = False
	input_pointer = 0
	output_pointer = 0
	output = []
	inputs = []

	def __init__(self, code, memory_amount=2000000):
		self.program = code.copy()
		
		for i in range(0, memory_amount):
			self.program.append(0)

		self.instruction_pointer = 0
		self.is_halted = False
		self.is_initialized = False
		self.is_waiting_for_input = False
		self.input_pointer = 0
		self.output_pointer = 0
		self.output = []
		self.inputs = []
		
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
			
	def instruction_add(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
		
		self.program[address_of_result] = operand_1 + operand_2
		
		opcode_signature_size = 4
		
		return opcode_signature_size

	def instruction_multiply(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
		
		self.program[address_of_result] = operand_1 * operand_2
		
		opcode_signature_size = 4
		
		return opcode_signature_size
		
	def instruction_input(self, parameter_modes):
		address_of_result = self.fetch_address_of_result(self.instruction_pointer, 0, parameter_modes, self.program)
		
		if self.input_pointer >= len(self.inputs):
			self.is_waiting_for_input = True
			opcode_signature_size = 0
		else:
			self.is_waiting_for_input = False
			
			self.program[address_of_result] = self.inputs[self.input_pointer]
			
			self.input_pointer += 1
			opcode_signature_size = 2
		
		return opcode_signature_size
	
	def instruction_output(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		self.output.append(operand_1)
		
		opcode_signature_size = 2
		
		return opcode_signature_size
	
	def instruction_jump_if_not_zero(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		
		if operand_1 != 0:
			self.instruction_pointer = operand_2
			opcode_signature_size = 0
		else:
			opcode_signature_size = 3
			
		return opcode_signature_size
		
	def instruction_jump_if_zero(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		
		if operand_1 == 0:
			self.instruction_pointer = operand_2
			opcode_signature_size = 0
		else:
			opcode_signature_size = 3
			
		return opcode_signature_size
		
	def instruction_less_then(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
		
		if operand_1 < operand_2:
			self.program[address_of_result] = 1
		else:
			self.program[address_of_result] = 0
			
		opcode_signature_size = 4
			
		return opcode_signature_size
		
	def instruction_equal_to(self, parameter_modes):
		operand_1 = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		operand_2 = self.fetch_parameter_value(self.instruction_pointer, 1, parameter_modes, self.program)
		address_of_result = self.fetch_address_of_result(self.instruction_pointer, 2, parameter_modes, self.program)
		
		if operand_1 == operand_2:
			self.program[address_of_result] = 1
		else:
			self.program[address_of_result] = 0
			
		opcode_signature_size = 4
			
		return opcode_signature_size
		
	def instruction_move_relative_memory_pointer(self, parameter_modes):
		offset = self.fetch_parameter_value(self.instruction_pointer, 0, parameter_modes, self.program)
		
		self.relative_memory_pointer += offset
		opcode_signature_size = 2
			
		return opcode_signature_size

	def instruction_halt(self, parameter_modes):
		self.is_halted = True
	
		return 0
	
	handler_map = { 1 : instruction_add
				   ,2 : instruction_multiply
				   ,3 : instruction_input
				   ,4 : instruction_output
				   ,5 : instruction_jump_if_not_zero
				   ,6 : instruction_jump_if_zero
				   ,7 : instruction_less_then
				   ,8 : instruction_equal_to
				   ,9 : instruction_move_relative_memory_pointer
				   ,99 : instruction_halt
				  }

	def run(self, inputs):
		self.input_pointer = 0
		self.output_pointer = 0
		self.output = []
		self.inputs = inputs.copy()
		
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
			
			handler = self.handler_map.get(opcode)

			if handler == None:
				raise ValueError("Unknown opcode: " + opcode)
			else:
				opcode_signature_size = handler(self, parameter_modes)
				
			self.instruction_pointer += opcode_signature_size
			
			if self.is_halted or self.is_waiting_for_input :
				break
			
		return self.output