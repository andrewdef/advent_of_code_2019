def calculate_fuel_requirment(mass):
	requirement = int(mass/3) - 2
	if requirement <= 0:
		return 0
	else:
		return (requirement + calculate_fuel_requirment(requirement))

total = 0
number_of_rockets = 0
with open('input.txt') as fd:
	for line in fd.readlines():
		number_of_rockets += 1
		mass = int(line)
		total += calculate_fuel_requirment(mass)
		
print(total)
print(number_of_rockets)
		