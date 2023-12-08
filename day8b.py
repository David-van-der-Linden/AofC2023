from my_secrets import path
import re
import sys

input_file = 'input8.txt'

# idea parse input put into dict where all entries are of the form
# key : [left location, right location]

with open(path + input_file) as f:
    lines = f.read().split('\n')

instructions = lines[0]
map = {}

for line_index in range(2, len(lines)):
    line = lines[line_index]
    key = re.split(' = ', line)[0]
    left_location = re.split(', ',re.split(' = ', line)[1])[0][1:]
    right_location = re.split(', ',re.split(' = ', line)[1])[1][:-1]
    
    map[key] = [left_location, right_location]

# finding starting locations
my_locations = []
for key in map:
	if key[2] == 'A':
		my_locations.append(key)

nr_of_steps = 0
print(my_locations)

while nr_of_steps < 20:
	for character in instructions:
		good_locations = 0
		for location_index in range(len(my_locations)):
			if my_locations[location_index][2] == 'Z':
				# then this location is good
				good_locations += 1
			
			# go to next
			if character == 'L':
				my_locations[location_index] = map[my_locations[location_index]][0]
			elif character == 'R':
				my_locations[location_index] = map[my_locations[location_index]][1]
			else:
				raise
		
		print(character)
		print(good_locations)
		print(my_locations)

		if good_locations == len(my_locations):
			print(my_locations)
			print('we made it')
			print(nr_of_steps)
			sys.exit()
		nr_of_steps += 1
    
print(my_locations)
print(nr_of_steps)