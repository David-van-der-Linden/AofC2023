import re
import numpy as np
from my_secrets import path

with open(path + 'input5.txt') as f:
    blocks = f.read().split('\n\n')

seeds = [int(seed) for seed in blocks[0].split(': ')[1].split()]
# print(seeds)

def make_dict(block):
    my_dict = {}
    lines = block.split('\n')
    for line_index in range(1, len(lines)):
        line = lines[line_index]
        # print(line)
        # print(line.split())
        destination_range_start, source_range_start, range_lenght = int(line.split()[0]), int(line.split()[1]), int(line.split()[2])
        for i in range(range_lenght):
            my_dict[source_range_start + i] = destination_range_start + i
    return my_dict

def map_to(seed, dict):
    if seed in dict:
        return dict[seed]
    else:
        return seed

# seed2soil           = make_dict(blocks[1])
# soil2fertilizer     = make_dict(blocks[2])
# fertilizer2water    = make_dict(blocks[3])
# water2light         = make_dict(blocks[4])
# light2temperature   = make_dict(blocks[5])
# temperature2humidity= make_dict(blocks[6])
# humidity2location   = make_dict(blocks[7])

d1 = make_dict(blocks[1])
print('block 1 done')
d2 = make_dict(blocks[2])
print('block 2 done')
d3 = make_dict(blocks[3])
print('block 3 done')
d4 = make_dict(blocks[4])
print('block 4 done')
d5 = make_dict(blocks[5])
print('block 5 done')
d6 = make_dict(blocks[6])
print('block 6 done')
d7 = make_dict(blocks[7])
print('block 7 done')

lowest_location = 99999999999999999999999999999999999999999999999999

for seed in seeds:
    location = map_to(map_to(map_to(map_to(map_to(map_to(map_to(seed, d1),d2),d3),d4),d5),d6),d7)
    if location < lowest_location:
        lowest_location = location
        lowest_seed = seed

print(lowest_location, lowest_seed)