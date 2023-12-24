from my_secrets import path
import re
import numpy as np
from collections import Counter
import portion as P

# todo improve explanation
# idea scan problem from top to and add the area pre iteration
# when we have
# ..c...c...
# ..........
# .cc...c..c
# ..........
# ........cc
# .c.c......
# ...c....c.
# where each c stands for the corner of a coordinate we have found
# we can compute the area at the top by between every other coordinate
# the area below that will have the same width until we hit more coordinates
# we can update the intervals by maintaining what was at the top and removing
# coordinates from out list if we have duplicates
# this works for computing the area between layers with coordinates
# then for computing the area at a layer with coordinates
# we take the union of the intervals above it and the new coordinates to be added

with open(path + 'input18.txt') as f:
    lines = f.read().split('\n')

# direction to relative (x, y)
dirs = {'R': np.array([1, 0]),
        'L': np.array([-1, 0]),
        'U': np.array([0, 1]),
        'D': np.array([0, -1])}

# finding cords
current = np.array([0, 0])
cords = {tuple(current)}
for line in lines:
    dir = line[0]
    steps = int(re.search('[0-9]+', line).group())
    current = current + steps * dirs[dir]
    cords.add(tuple(current))

all_y = sorted(set([cord[1] for cord in cords]))[::-1]
all_y.append(all_y[-1]-1)

ans = 0
current_top = []
for y_index in range(len(all_y)-1):
    y = all_y[y_index]
    next_y = all_y[y_index + 1]
    hight_between = y - 1 - next_y

    new_to_top = sorted([cord[0] for cord in cords if cord[1] == y])
    # at y top
    interval = P.empty()
    for i in range(0, len(current_top), 2):
        interval = interval | P.closed(current_top[i], current_top[i + 1] + 1)
    for i in range(0, len(new_to_top), 2):
        interval = interval | P.closed(new_to_top[i], new_to_top[i + 1] + 1)
    width_at_y = 0
    for subint in interval:
        width_at_y += subint.upper - subint.lower

    # update current_top
    current_top.extend(new_to_top)
    current_top = [k for k, v in Counter(current_top).items() if v == 1]
    current_top = sorted(current_top)

    # compute width_between
    width_between = 0
    for i in range(0, len(current_top), 2):
        width_between += current_top[i + 1] - current_top[i] + 1

    # compute area
    area = width_between * hight_between + width_at_y
    ans += area

print(ans)
