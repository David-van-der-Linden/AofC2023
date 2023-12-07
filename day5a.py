import re
import numpy as np
from my_secrets import path
import time

with open(path + 'input5.txt') as f:
    blocks = f.read().split('\n\n')

seeds = [int(seed) for seed in blocks[0].split(': ')[1].split()]

for block_index in range(1,len(blocks)):
    blocks[block_index] = blocks[block_index].split('\n')

min_key = 99999999999999999999999999999

tik = time.time()
for seed in seeds:
    key = seed
    print('seed', key)
    for block_index in range(1,len(blocks)):
        block = blocks[block_index]
        # print('block_index', block_index)
        for line_index in range(1,len(block)):
            # print('line index:', line_index)
            destination_range_start, source_range_start, range_lenght = int(block[line_index].split()[0]), int(block[line_index].split()[1]), int(block[line_index].split()[2])
            if key >= source_range_start and key < source_range_start + range_lenght:
                key = destination_range_start + key - source_range_start
                # print('key', key)
                # print('time to break!')
                break
    min_key = min(min_key,key)
    
print(min_key)

tak = time.time()
print(tak-tik)
print(len(seeds))