def find_the_path(starting_point, destination, previous_point, path):
	path.append(starting_point)
	
	if starting_point == destination:
		return True
	
	for point in connections[starting_point]:
		if previous_point != point:
			subpath = []
			found = find_the_path(point, destination, starting_point, subpath)
			
			if found:
				for x in subpath:
					path.append(x)
				return True
				
	return False

connections = {}

with open('input.txt') as fd:
	for line in fd.read().split('\n'):

		object = line.split(')')[1]
		orbited_object = line.split(')')[0]
		
		if connections.get(object) == None:
			connections[object] = []
			
		if connections.get(orbited_object) == None:
			connections[orbited_object] = []

		connections[object].append(orbited_object)
		connections[orbited_object].append(object)

path = []
found = find_the_path('YOU', 'SAN', None, path)

if found:
	print(path)
	print('Transfers: ' + str(len(path) - 3))
else:
	print('Path not found')