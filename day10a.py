from math import ceil
import re
import numpy as np
from my_secrets import path

with open(path + 'input10.txt') as f:
    lines = f.read().split('\n')

# idea
# go trough the entire path starting next to s and ending next to s
# store last node current node and use this to compute what the next node is
# keep track of the amount of steps needed to reach the end then divide by 2 with some rounding

# find starting point
for line_index in range(len(lines)):
    line = lines[line_index]
    col_s = re.search('S', line)
    if col_s:
        col_s = col_s.span()[0]
        row_s = line_index
        break

get_ends = {'|': [[-1, 0], [1, 0]],
            '-': [[0, -1], [0, 1]],
            'L': [[-1, 0], [0, 1]],
            'J': [[0, -1], [-1, 0]],
            '7': [[0, -1], [1, 0]],
            'F': [[1, 0], [0, 1]]}


def get_next(row_l: int, col_l: int, row_c: int, col_c: int, symbol: str):
    # reruns coordinates of the next symbol along the path
    # or raises error
    last = np.array([row_l, col_l])
    current = np.array([row_c, col_c])

    # idea
    # for symbol get relative positions and check which one already occupied
    ends = get_ends[symbol]
    if (last == current + np.array(ends[0])).all():
        out = current + np.array(ends[1])
        return out[0], out[1]
    elif (last == current + np.array(ends[1])).all():
        out = current + np.array(ends[0])
        return out[0], out[1]
    else:
        raise 'ends not match current and last'


# from looking at the puzzle input we deduced that the start node should be a '-'
# let us chose to start on the right of S and end on the left of S
row_l = row_s
col_l = col_s
row_c = row_s
col_c = col_s + 1

steps = 1
while (row_c, col_c) != (row_s, col_s - 1):   # input
    # while (row_c, col_c) != (row_s + 1, col_s):     # test_input
    row_n, col_n = get_next(row_l, col_l, row_c, col_c, lines[row_c][col_c])
    row_l, col_l, row_c, col_c = row_c, col_c, row_n, col_n
    steps += 1

ans = ceil((steps+1)/2)
print(ans)
