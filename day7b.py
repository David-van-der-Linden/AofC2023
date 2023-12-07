import math
import re
from my_secrets import path

input_file = 'input7.txt'

# compare hands
# print('A'>='')
# if we map capetal leters to lowercase letters we can use string comparison for which hand wins given there the same type
cap_to_lower = {'A': 'z',
				'K': 'y',
				'Q': 'x',
				'J': '.',
				'T': 'v'}
# print('1234z'>='1234y')

# idea parse all replace letters acording to cap_to_lower
# add a symbol at the start indicating which hand type it is and then apply a sorting algorithm to it

def determin_type(str):
	temp_dict = {}
	# print(str)

	for car in str:
		# print(car)
		if car in temp_dict:
			temp_dict[car] += 1
		else:
			temp_dict[car] = 1
	
	# print(temp_dict)

    # akey will be the caracter that occurs the most and bkey the caracter that occurs the second most
    # maxa and maxb will be temp_dict[akey] and temp_dict[bkey] respectivly
	maxa = 0
	maxb = 0
	akey = 'none'
	bkey = 'none'
	jokers = 0
	
	for key in temp_dict:
		if key == '.':
			jokers = temp_dict[key]
		elif temp_dict[key] >= maxa:
			maxb = maxa
			bkey = akey
			maxa = temp_dict[key]
			akey = key
		elif temp_dict[key] > maxb:
			maxb = temp_dict[key]
			bkey = key

	# print(akey)


	if maxa + jokers == 5:
		#type 5 of a kind
		return 'g'
	elif maxa + jokers == 4:
		# type 4 of a kind
		return 'f'
	elif (maxa + jokers == 3 and maxb == 2) or (maxa == 3 and maxb + jokers == 2):
		# type full house
		return 'e'
	elif maxa + jokers == 3:
		# type 3 of a kind
		return 'd'
	elif maxa == 2 and maxb == 2:
		# type 2 pair
		return 'c'
	elif maxa + jokers == 2:
		# type 1 pair
		return 'b'
	else:
		# type high card
		return 'a'


# --------------- replacing AKQJT ----------------------
# Read in the file
with open(path + input_file) as file:
  filedata = file.read()
# Replace the target string
for key in cap_to_lower:
	filedata = filedata.replace(key, cap_to_lower[key])
# Write the file out again
with open(path + 'prosessed_' + input_file, 'w') as file:
  file.write(filedata)

# ------------------ adding the symbol at the start of the line ---------
import fileinput
import sys

for line in fileinput.input([path + 'prosessed_' + input_file], inplace=True):
    sys.stdout.write('{t}{l}'.format(l=line, t=determin_type(line.split()[0])))

with open(path + 'prosessed_' + input_file) as f:
    lines = f.read().split('\n')

lines.sort()

ans = 0
for count, line in enumerate(lines):
	rank = count + 1
	bet = int(line.split()[1])
	ans += rank*bet

print(ans)