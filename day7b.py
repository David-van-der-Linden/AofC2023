import math
import re
from my_secrets import path
from collections import Counter

input_file = 'input7.txt'

# compare hands
# print('A'>='')
# if we map capital letters to lowercase letters we can use string comparison for which hand wins given there the same type
cap_to_lower = {'A': 'z',
				'K': 'y',
				'Q': 'x',
				'J': '.',
				'T': 'v'}
# print('1234z'>='1234y')

# idea parse all replace letters according to cap_to_lower
# add a symbol at the start indicating which hand type it is and then apply a sorting algorithm to it

def determine_type(str):
	# input str is a string of length 5 
	# returns single character string between a and g 
	# where g corresponds to the best hand type and a to the worst hand type
	
	# dictionary that counts how often a character occurs in a string
	temp_dict = {}
	for car in str:
		# print(car)
		if car in temp_dict:
			temp_dict[car] += 1
		else:
			temp_dict[car] = 1
	
	# print(temp_dict)

    # a_key will be the character that occurs the most and b_key the character that occurs the second most,
    # a_val and b_val will be temp_dict[a_key] and temp_dict[b_key] respectively.
	a_val = 0
	b_val = 0
	a_key = 'none'
	b_key = 'none'
	jokers = 0
	
	for key in temp_dict:
		if key == '.':
			jokers = temp_dict[key]
		elif temp_dict[key] >= a_val:
			b_val = a_val
			b_key = a_key
			a_val = temp_dict[key]
			a_key = key
		elif temp_dict[key] > b_val:
			b_val = temp_dict[key]
			b_key = key

	# logic for determining which hand type we have
	if a_val + jokers == 5:
		#type 5 of a kind
		return 'g'
	elif a_val + jokers == 4:
		# type 4 of a kind
		return 'f'
	elif (a_val + jokers == 3 and b_val == 2) or (a_val == 3 and b_val + jokers == 2):
		# type full house
		return 'e'
	elif a_val + jokers == 3:
		# type 3 of a kind
		return 'd'
	elif a_val == 2 and b_val == 2:
		# type 2 pair
		return 'c'
	elif a_val + jokers == 2:
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
with open(path + 'processed_' + input_file, 'w') as file:
  file.write(filedata)

# ------------------ adding the symbol at the start of the line ---------
import fileinput
import sys

for line in fileinput.input([path + 'processed_' + input_file], inplace=True):
    sys.stdout.write('{t}{l}'.format(l=line, t=determine_type(line.split()[0])))

with open(path + 'processed_' + input_file) as f:
    lines = f.read().split('\n')

lines.sort()

ans = 0
for count, line in enumerate(lines):
	rank = count + 1
	bet = int(line.split()[1])
	ans += rank*bet

print(ans)