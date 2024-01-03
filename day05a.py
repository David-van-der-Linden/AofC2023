import numpy as np
from my_secrets import path

with open(path + 'input5.txt') as f:
    blocks = f.read().split('\n\n')

seeds = [int(seed) for seed in blocks[0].split(': ')[1].split()]

for block_index in range(1, len(blocks)):
    blocks[block_index] = blocks[block_index].split('\n')

# idea follow reasoning just like in the examples for all possible seeds

min_key = np.inf
for seed in seeds:
    key = seed
    for block_index in range(1, len(blocks)):
        block = blocks[block_index]
        for line_index in range(1, len(block)):
            destination_range_start = int(block[line_index].split()[0])
            source_range_start = int(block[line_index].split()[1])
            range_length = int(block[line_index].split()[2])
            if key >= source_range_start and key < source_range_start + range_length:
                key = destination_range_start + key - source_range_start
                break
    min_key = min(min_key, key)

print(min_key)
