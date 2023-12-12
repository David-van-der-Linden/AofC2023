from os import remove
import re
import numpy as np
from my_secrets import path

with open(path + 'test12.txt') as f:
    lines = f.read().split('\n')

# idea brute force all possible combinations and count the ones that work
# needed:
# 1. A way to convert string of .'s and #'s to the corresponding sequence of numbers
# 2. A way of turning string of .'s, #'s, and ?'s into all possible strings
# where ?'s are replaced by .'s and #'s
# 3. A way of counting all the correct strings

# ideas for speeding up
# discard strings that have to many #

# 1
def compute_seq(input_str : str):
    # returns sequence in list form '#.#.###' -> [1, 1, 3]
    # the size of each contiguous group of damaged springs 
    # is listed in the order those groups appear in the row
    return [len(str) for str in re.findall('#+', input_str)]

# 2
def get_all_str(input_list : list, max_hash : int):
    # input list of string containing ?'s
    # returns list of strings not containing ?'s

    to_return = []
    for str in input_list:
        question_index = str.find('?')
        # if no hit
        if question_index == -1:
            # then schedule this string for return
            to_return.append(str)
        else:
            # replace one character at the time and iterate
            for str_2 in get_all_str([str[:question_index]+'.'+str[(question_index+1):]], max_hash):
                to_return.append(str_2)
            for str_3 in get_all_str([str[:question_index]+'#'+str[(question_index+1):]], max_hash):
                to_return.append(str_3)
    
    # print('to_return_pre', to_return)
    to_return = [str for str in to_return if sum(compute_seq(str)) <= max_hash]
    # print('to_return_post', to_return)
    return to_return

# 3
ans = 0
for line in lines:
    split_line = line.split()
    temp_str = split_line[0]
    input_str = temp_str + '?' + temp_str + '?' + temp_str + '?' + temp_str + '?' + temp_str 
    temp_seq = [int(val) for val in split_line[1].split(',')]
    desired_seq = temp_seq + temp_seq + temp_seq + temp_seq + temp_seq

    print()
    print('input_str', input_str)
    print('desired_seq', desired_seq)
    ways = 0
    max_hash = sum(desired_seq)
    print('max_hash', max_hash)
    for str in get_all_str(input_list=[input_str], max_hash=max_hash):
        # print('str:', str)
        # print(compute_seq(str))
        if compute_seq(str) == desired_seq:
            ways += 1
    print('ways:', ways)
    ans += ways

print('ans:', ans)