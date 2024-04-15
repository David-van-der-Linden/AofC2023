from my_secrets import path
import re

input_file = 'input8.txt'

# idea parse input put into dict where all entries are of the form
# key : [left location, right location]

with open(path + input_file) as f:
    lines = f.read().split('\n')

instructions = lines[0]
mapper = {}

for line_index in range(2, len(lines)):
    line = lines[line_index]
    key = re.split(' = ', line)[0]
    left_location = re.split(', ', re.split(' = ', line)[1])[0][1:]
    right_location = re.split(', ', re.split(' = ', line)[1])[1][:-1]

    mapper[key] = [left_location, right_location]

my_location = 'AAA'

nr_of_steps = 0
while my_location != 'ZZZ':
    for character in instructions:
        print(my_location)
        if my_location == 'ZZZ':
            print('we made it')
        if character == 'L':
            my_location = mapper[my_location][0]
        elif character == 'R':
            my_location = mapper[my_location][1]
        else:
            raise AssertionError()

        nr_of_steps += 1

print(my_location)
print(nr_of_steps)
