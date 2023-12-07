from my_secrets import path

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
# neutral_slack = key - max(source_r_s + range_lenght - 1 st its les than key) + 1
# active_slack comes form using an interval to transform to the next key and 
# then the slack is how much lower it could have been while stil using the same interval
# so when 
# 10, 5, 5
# with key 6 the slack is 1
# active_slack = key - source_r_s
# per transformation there will be slack ither the neutral or ative slack
# the total slack will be the miniumum of all of them
# 
# foor each seed there is a total_slack, and we know that
# loc(seed-total_slack) = loc(seed) - total_slack
#
# because of this we only need to compute first at the top of the interval
# next_seed = seed - totalslack - 1
# given next seed is still in the interval if not then
# the bottem of the interval can be computed and compared to the seed - total_slacks

locmin = 999999999999999999999999999999

nr_of_seeds = 0
for range_index in range(int(len(ranges)/2)):
    nr_of_seeds += ranges[range_index*2+1]

print(nr_of_seeds)

for range_index in range(int(len(ranges)/2)):
    range_min = ranges[range_index*2]
    print('range_min', range_min)
    range_max = ranges[range_index*2]+ranges[range_index*2+1]-1
    print('range_max', range_max)

    # init
    seed = range_max
    while seed >= range_min:
        def get_loc():
            key = seed
            slack = 999999999999999999999999999999999999999999
            # print('seed', key)
            for block_index in range(1,len(blocks)):
                block = blocks[block_index]
                # print('block_index', block_index)
                neutral_slack = 99999999999999999999999999999
                for line_index in range(1,len(block)):
                    # print('line index:', line_index)
                    destination_range_start, source_range_start, range_lenght = int(block[line_index].split()[0]), int(block[line_index].split()[1]), int(block[line_index].split()[2])
                    if key >= source_range_start and key < source_range_start + range_lenght:
                        # active slack
                        slack = min(slack, key-source_range_start)
                        key = destination_range_start + key - source_range_start
                        # print('key', key)
                        # print('time to break!')
                        break
                    elif source_range_start + range_lenght <= key:
                        neutral_slack = min(neutral_slack, key - source_range_start - range_lenght + 1)
                # neutral slack
                slack = min(slack, neutral_slack)
            return key, slack
        
        loc, slack = get_loc()
        if seed == range_min:
            # print('if')
            locmin = min(locmin,loc)
            break
        elif seed - slack > range_min:
            # print('elif')
            locmin = min(locmin,loc - slack)
            seed = seed - slack - 1
        else:
            # print('else')
            seed = range_min
    
    
print('locmin', locmin)