import datetime
import math

def apply_gravity(objects):
	for i in range(0, len(objects)):
		object_1 = objects[i]
		
		for k in range(i + 1, len(objects)):
			object_2 = objects[k]
			
			for j in range(3):
				pos_1 = object_1[0][j]
				pos_2 = object_2[0][j]
				
				if pos_1 > pos_2:
					object_1[1][j] -= 1
					object_2[1][j] += 1
				elif pos_1 < pos_2:
					object_1[1][j] += 1
					object_2[1][j] -= 1
				
def apply_velocity(objects):
	for object in objects:
		for j in range(3):
			object[0][j] += object[1][j]

def create_state_key(state):
	state_key_x = []
	state_key_y = []
	state_key_z = []
	
	for object in state:
		state_key_x.append(str(object[0][0]))
		state_key_x.append(str(object[1][0]))
		
	for object in state:
		state_key_y.append(str(object[0][1]))
		state_key_y.append(str(object[1][1]))
		
	for object in state:
		state_key_z.append(str(object[0][2]))
		state_key_z.append(str(object[1][2]))
			
	return ('-'.join(state_key_x), '-'.join(state_key_y), '-'.join(state_key_z))
	
def save_state(state_to_save, saved_states_list, state_index):
	key = create_state_key(state_to_save)
	
	saved_states_list[0][key[0]] = state_index
	saved_states_list[1][key[1]] = state_index
	saved_states_list[2][key[2]] = state_index
	
def find_same_state(current_state, previous_states, iteration):
	key = create_state_key(current_state)
	
	found_state_x = previous_states[0].get(key[0])
	found_state_y = previous_states[1].get(key[1])
	found_state_z = previous_states[2].get(key[2])
	
	return (found_state_x, found_state_y, found_state_z)

def lcm(a, b):
	 return int(a * b / math.gcd(a, b))
	 
def run():				
	objects = []
	with open('input.txt') as fd:
		for line in fd.read().split('\n'):
			object = [[0, 0, 0], [0, 0, 0]]
			
			info = line[1:len(line) - 1].split(',')
			
			for item in info:
				key = (item.split('=')[0]).strip()
				value = int(item.split('=')[1])

				if key == 'x':
					object[0][0] = value
				elif key == 'y':
					object[0][1] = value
				elif key == 'z':
					object[0][2] = value
					
			objects.append(object)

	TIME_STEPS = 100000000
	previous_states = [{}, {}, {}]
	save_state(objects, previous_states, 0)

	start = datetime.datetime.now()
	
	period_x = None
	period_y = None
	period_z = None

	for i in range(1, TIME_STEPS + 1):
		if i % 10000000 == 0 and i != 1:
			print('Iteration ', i)
			print('Elapsed: ', datetime.datetime.now() - start)
			
			start = datetime.datetime.now()

		#print(objects)
		apply_gravity(objects)
		apply_velocity(objects)
		
		previous_state_same = find_same_state(objects, previous_states , i)
		
		if previous_state_same[0] != None:
			period_x = i - previous_state_same[0]
	
		if previous_state_same[1] != None:
			period_y = i - previous_state_same[1]

		if previous_state_same[2] != None:
			period_z = i - previous_state_same[2]			
			
		if period_x != None and period_y != None and period_z != None:
			print('Period x: ', period_x)
			print('Period y: ', period_y)
			print('Period z: ', period_z)
			
			gcd = math.gcd(math.gcd(period_x, period_y), period_z)
			
			print('Total period: ' , lcm(period_x, lcm(period_y, period_z)))
			break
		else:
			save_state(objects, previous_states, i)
	
run()
	
