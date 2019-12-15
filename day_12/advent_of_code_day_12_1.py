def apply_gravity(objects):
	for i in range(0, len(objects)):
		object_1 = objects[i]
		
		for k in range(i + 1, len(objects)):
			object_2 = objects[k]
			
			for j in range(3):
				pos_1 = object_1[j]
				pos_2 = object_2[j]
				
				if pos_1 > pos_2:
					object_1[3][j] -= 1
					object_2[3][j] += 1
				elif pos_1 < pos_2:
					object_1[3][j] += 1
					object_2[3][j] -= 1
				
def apply_velocity(objects):
	for object in objects:
		for j in range(3):
			object[j] += object[3][j]
			
def calculate_total_energy(objects):
	total = 0
	
	for object in objects:
		potential_energy = 0
	
		potential_energy += abs(object[0])
		potential_energy += abs(object[1])
		potential_energy += abs(object[2])
		
		kinetic_energy = 0
		for x in object[3]:
			kinetic_energy += abs(x)
			
		total += kinetic_energy * potential_energy
			
	return total
				
objects = []
with open('input.txt') as fd:
	for line in fd.read().split('\n'):
		object = [0, 0, 0, [0, 0, 0]]
		
		info = line[1:len(line) - 1].split(',')
		
		for item in info:
			key = (item.split('=')[0]).strip()
			value = int(item.split('=')[1])

			if key == 'x':
				object[0] = value
			elif key == 'y':
				object[1] = value
			elif key == 'z':
				object[2] = value
				
		objects.append(object)
		
print(objects)

TIME_STEPS = 1000

for i in range(0, TIME_STEPS):
	apply_gravity(objects)
	apply_velocity(objects)
	
	print(objects)
	
	energy = calculate_total_energy(objects)
	print(energy)
	
