def count_orbits_for_object(object, orbits):
	orbited_object = orbits.get(object)

	if orbited_object == None:
		return 0
	else:
		return 1 + count_orbits_for_object(orbited_object, orbits)

orbits = {}

with open('input.txt') as fd:
	for line in fd.read().split('\n'):

		object = line.split(')')[1]
		orbited_object = line.split(')')[0]
		
		if orbits.get(object):
			raise ValueError('Object ' + object + 'orbits multiple object')
		else:
			orbits[object] = orbited_object

total_orbits = 0

for object in orbits:
	orbits_for_object = count_orbits_for_object(object, orbits)
	
	print(object + ' orbits ' + str(orbits_for_object) + ' objects ')
	
	total_orbits += orbits_for_object
	
print(total_orbits)