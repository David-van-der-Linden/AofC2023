from my_secrets import path
import re
import sys
import numpy as np
from math import lcm

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
    left_location = re.split(', ', re.split(' = ', line)[1])[0][1:]
    right_location = re.split(', ', re.split(' = ', line)[1])[1][:-1]

    map[key] = [left_location, right_location]

# finding starting locations
my_locations = []
for key in map:
    if key[2] == 'A':
        my_locations.append(key)

nr_of_steps = 0
print('starting locations', my_locations)

final_states = [[] for _ in range(len(my_locations))]
final_steps = [[] for _ in range(len(my_locations))]
final_chars = [[] for _ in range(len(my_locations))]

info_gathered = 0

flag = True
while flag:
    for character_index in range(len(instructions)):
        character = instructions[character_index]

        # when one of the locations is good store info
        for location_index in range(len(my_locations)):
            if my_locations[location_index][2] == 'Z':
                final_states[location_index].append(
                    my_locations[location_index])
                final_steps[location_index].append(nr_of_steps)
                final_chars[location_index].append(character_index)
                info_gathered += 1

                # check if we have enough info
                if info_gathered >= 50:
                    print(final_states)
                    print(final_steps)
                    print(final_chars)
                    flag = False

        # if good_locations == len(my_locations):
        # if good_locations >= 1:
        # 	print('my_locations', my_locations)
        # 	print('nr_of_steps', nr_of_steps)
        # 	print('character_index', character_index)
            # sys.exit()

        # go to next
        for location_index in range(len(my_locations)):
            if character == 'L':
                my_locations[location_index] = map[my_locations[location_index]][0]
            elif character == 'R':
                my_locations[location_index] = map[my_locations[location_index]][1]
            else:
                raise
        nr_of_steps += 1


# print(my_locations)
# print(nr_of_steps)

# first hit
# 12169
# 20093
# 20659
# 22357
# 13301
# 18961


# idea
# each ghost will end up in a loop eventually
# assuming the puzzle has a solution we can deduce that
# each loop must have at least one location that ends with a Z in it
# when visiting such a location we can keep track of where we are in the instruction sequence
# if we visit the same location and are at the same point in the instruction sequence
# and did not visit the location in the meantime then the number of steps between these instances is the length of the loop
# if there are multiple locations then end with a Z in the same loop then the math for the next part will become more complex
# however that does not seem to be needed for this problem input
# also for this input we only seem to reach ending locations whenever where at the end of the instruction sequence

# git1 = first time visiting location for ghost i
# git2 = second time visiting location for ghost i
# loop_size_gi = git2 - git1

# ghost i will be in a final state if and only if
# (number_of_steps % loop_size_gi == git1 % loop_size_gi) and (number_of_steps >= git1)

# when this holds for all i then we have that all ghosts are in a final state
# we can find the fist number_of_steps for which this is the case by letting
# number_of_steps = loop_size_gi*m + git1, where i is argmax_i(loop_size_gi)
# and trying for increasing m

loop_size = [0 for _ in range(len(my_locations))]

for i in range(len(my_locations)):
    # final_steps[0] # git1
    # final_steps[1] # git2
    loop_size[i] = final_steps[i][1] - final_steps[i][0]

index_max = np.argmax(loop_size)

# for m in range(999999999):
# 	nr_of_steps = loop_size[index_max]*m + final_steps[index_max][0]

# 	if m % 100000 == 0:
# 		print(nr_of_steps)

# 	nr_of_good_ones = 0
# 	for i in range(len(my_locations)):
# 		# (number_of_steps % loop_size_gi == git1 % loop_size_gi) and (number_of_steps >= git1)
# 		if (nr_of_steps % loop_size[i] == final_steps[i][0] % loop_size[i]) and (nr_of_steps >= final_steps[i][0]):
# 			# then this one is good
# 			nr_of_good_ones += 1

# 	if nr_of_good_ones == len(my_locations):
# 		print(nr_of_steps)
# 		print('thats it')
# 		sys.exit()

# the above code is to slow but as it turns out
# if we look at the loop sises we can see that
# loop_size[i] == git1
# this makes it so that the least common multiple of all loops is the answer
# let us verify this claim using the above code again

nr_of_steps = lcm(12169, 20093, 20659, 22357, 13301, 18961)

nr_of_good_ones = 0
for i in range(len(my_locations)):
    # (number_of_steps % loop_size_gi == git1 % loop_size_gi) and (number_of_steps >= git1)
    if (nr_of_steps % loop_size[i] == final_steps[i][0] % loop_size[i]) and (nr_of_steps >= final_steps[i][0]):
        # then this one is good
        nr_of_good_ones += 1

if nr_of_good_ones == len(my_locations):
    print(nr_of_steps)
    print('thats it')
    sys.exit()
