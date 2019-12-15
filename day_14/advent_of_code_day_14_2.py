from nanofactory import NanoFactory, OutOfOreException, Reaction, ReactionBook
import math

reactions = ReactionBook()
reactions.init_from_file('input.txt')

STARTING_ORE = 1000000000000
factory = NanoFactory(reactions, STARTING_ORE)

factory.produce_chemical('FUEL', 1)
needed_ore_for_1_fuel = factory.consumed_ore

out_of_ore = False
while( not out_of_ore ):
	rate = max(math.floor(factory.available_ore / needed_ore_for_1_fuel), 1)

	try:
		factory.produce_chemical('FUEL', rate)
	except OutOfOreException as e:
		out_of_ore = True

print(factory.available_chemicals['FUEL'])
		