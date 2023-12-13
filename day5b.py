from my_secrets import path
import numpy as np

with open(path + 'input5.txt') as f:
    blocks = f.read().split('\n\n')

ranges = [int(seed) for seed in blocks[0].split(': ')[1].split()]

for block_index in range(1,len(blocks)):
    blocks[block_index] = blocks[block_index].split('\n')

# slack is number of seeds that could have been used below so when 
# 10, 5, 5
# then seed 9 has a slack of 4
# and seed 10 has an slack of 0
# neutral_slack comes from identity transformations
# neutral_slack = key - max(source_r_s + range_length - 1 st its les than key) + 1
# active_slack comes form using an interval to transform to the next key and 
# then the slack is how much lower it could have been while still using the same interval
# so when 
# 10, 5, 5
# with key 6 the slack is 1
# active_slack = key - source_r_s
# per transformation there will be slack either the neutral or active slack
# the total_slack (or slack for short) will be the minimum of all of them
# 
# for each seed there is a total_slack, and we know that
# loc(seed-total_slack) = loc(seed) - total_slack
#
# because of this we only need to compute first at the top of the interval
# next_seed = seed - total_slack - 1
# given next seed is still in the interval if not then
# the bottom of the interval can be computed and compared to the seed - total_slacks

loc_min = np.inf

nr_of_seeds = 0
for range_index in range(int(len(ranges)/2)):
    nr_of_seeds += ranges[range_index*2+1]

for range_index in range(int(len(ranges)/2)):
    range_min = ranges[range_index*2]
    range_max = ranges[range_index*2]+ranges[range_index*2+1]-1

    seed = range_max
    while True:
        key = seed
        total_slack = np.inf
        for block_index in range(1,len(blocks)):
            block = blocks[block_index]
            neutral_slack = np.inf
            for line_index in range(1,len(block)):
                destination_range_start, source_range_start, range_length = int(block[line_index].split()[0]), int(block[line_index].split()[1]), int(block[line_index].split()[2])
                if key >= source_range_start and key < source_range_start + range_length:
                    # since in interval we update active slack
                    active_slack = key-source_range_start
                    total_slack = min(total_slack, active_slack)
                    key = destination_range_start + key - source_range_start
                    break
                elif source_range_start + range_length <= key:
                    # if not in interval update neutral slack
                    neutral_slack = min(neutral_slack, key - source_range_start - range_length + 1)
            total_slack = min(total_slack, neutral_slack)
        
        loc, slack = key, total_slack
        if seed == range_min:
            loc_min = min(loc_min, loc)
            break
        elif seed - slack > range_min:
            loc_min = min(loc_min, loc - slack)
            seed = seed - slack - 1
        else:
            seed = range_min

print('loc_min', loc_min)