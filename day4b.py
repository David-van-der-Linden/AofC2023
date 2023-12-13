import re
import numpy as np
from my_secrets import path

with open(path + 'input4.txt') as f:
    lines = f.read().split('\n')

amount_of_card = np.ones(len(lines))

for line_index in range(len(lines)):
    line = lines[line_index]
    split_line = line.split(':')[1]
    split_line = split_line.split('|')
    winning_nrs = re.findall('[0-9]+', split_line[0])
    nrs_on_card = re.findall('[0-9]+', split_line[1])

    nr_of_matches = 0
    for nr in nrs_on_card:
        if nr in winning_nrs:
            nr_of_matches += 1
    
    if nr_of_matches > 0:
        for i in range(line_index + 1, line_index + nr_of_matches+1):
            amount_of_card[i] += amount_of_card[line_index]
print(int(sum(amount_of_card)))