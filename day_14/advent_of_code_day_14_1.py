from nanofactory import NanoFactory, OutOfOreException, Reaction, ReactionBook
import math

reactions = ReactionBook()
reactions.init_from_file('input.txt')

factory = NanoFactory(reactions, None)
factory.produce_chemical('FUEL', 1)

print(factory.consumed_ore)