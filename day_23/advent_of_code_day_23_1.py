from common.intcodecomputer import CodeExecutor

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

network = []
packets = {}

for i in range(50):
	computer = CodeExecutor(program, memory_amount=2000)
	
	network.append(computer)
	packets[i] = []
	
found = False
while( not found ):
	for i in range(50):
		if not computer.is_initialized:
			incoming_packets = [i]
		else:
			incoming_packets = packets[i].copy()
		
		if len(incoming_packets) == 0:
			incoming_packets = [-1]
			
		packets[i] = []
		outgoing_packets = network[i].run(incoming_packets)

		for k in range(0, len(outgoing_packets), 3):
			address = outgoing_packets[k]
			x = outgoing_packets[k + 1]
			y = outgoing_packets[k + 2]
			
			if address == 255:
				print(y)
				found = True
				break
			else:
				if address not in packets:
					packets[address] = []

				packets[address].append(x)
				packets[address].append(y)