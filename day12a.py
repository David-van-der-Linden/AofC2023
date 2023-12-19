import re
import numpy as np
from my_secrets import path

with open(path + 'input12.txt') as f:
    lines = f.read().split('\n')

# idea brute force all possible combinations and count the ones that work
# needed:
# 1. A way to convert string of .'s and #'s to the corresponding sequence of numbers
# 2. A way of turning string of .'s, #'s, and ?'s into all possible strings
# where ?'s are replaced by .'s and #'s
# 3. A way of counting all the correct strings

# 1


def compute_seq(input_str: str):
    # returns sequence in list form '#.#.###' -> [1, 1, 3]
    # the size of each contiguous group of damaged springs
    # is listed in the order those groups appear in the row
    return [len(str) for str in re.findall('#+', input_str)]

# 2


def get_all_str(input_list: list):
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
            for str_2 in get_all_str([str[:question_index]+'.'+str[(question_index+1):]]):
                to_return.append(str_2)
            for str_3 in get_all_str([str[:question_index]+'#'+str[(question_index+1):]]):
                to_return.append(str_3)
    return to_return


# 3
ans = 0
for line in lines:
    split_line = line.split()
    input_str = split_line[0]
    desired_seq = [int(val) for val in split_line[1].split(',')]

    ways = 0
    for str in get_all_str(input_list=[input_str]):
        if compute_seq(str) == desired_seq:
            ways += 1
    print('ways:', ways)
    ans += ways

print('ans:', ans)
