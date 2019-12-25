from common.intcodecomputer import CodeExecutor

def network_is_idle(network):
	idle_computers = 0
	for info in network:
		if info[1] >= 3:
			idle_computers += 1
			
	if idle_computers == len(network):
		return True
	else:
		return False

def send_nat_packet(nat):
	nat_packet = nat['nat_packet']
	last_delivered_nat_packet = nat['last_delivered_nat_packet']

	if nat_packet == None:
		raise ValueError('Tried to use NAT packet before receiving one')

	incoming_packets = nat_packet.copy()
	if last_delivered_nat_packet != None and last_delivered_nat_packet[1] == nat_packet[1]:
		print(nat_packet[1])
		nat['found'] = True
		
	nat['last_delivered_nat_packet'] = nat_packet.copy()
	nat['nat_packet'] = None

	return incoming_packets

def add_nat_packet(nat, nat_packet):
	nat['nat_packet'] = nat_packet.copy()

program = []
with open('input.txt') as fd:
	program = [int(x) for x in fd.read().split(',')]

network = []
packets = {}

for i in range(50):
	computer = CodeExecutor(program, memory_amount=2000)
	
	network.append([computer, 0])
	packets[i] = []
	
nat = {}
nat['nat_packet'] = None
nat['last_delivered_nat_packet'] = None
nat['found'] = False

while( not nat['found'] ):
	for i in range(50):
		if not computer.is_initialized:
			incoming_packets = [i]
		else:
			incoming_packets = packets[i].copy()
		
		if len(incoming_packets) == 0:
			if i == 0 and network_is_idle(network):
				incoming_packets = send_nat_packet(nat)
			else:
				incoming_packets = [-1]
			
		packets[i] = []
		outgoing_packets = network[i][0].run(incoming_packets)
		
		if len(outgoing_packets) == 0:
			network[i][1] += 1
		else:
			network[i][1] = 0

		for k in range(0, len(outgoing_packets), 3):
			address = outgoing_packets[k]
			x = outgoing_packets[k + 1]
			y = outgoing_packets[k + 2]
			
			if address == 255:
				add_nat_packet(nat, [x, y])
			else:
				if address not in packets:
					packets[address] = []

				packets[address].append(x)
				packets[address].append(y)