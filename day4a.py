import re
from my_secrets import path

with open(path + 'input4.txt') as f:
    lines = f.read().split('\n')

ans = 0
for line in lines:
    split_line = line.split(':')[1]
    split_line = split_line.split('|')
    winning_nrs = re.findall('[0-9]+', split_line[0])
    nrs_on_card = re.findall('[0-9]+', split_line[1])

    nr_of_matches = 0
    for nr in nrs_on_card:
        if nr in winning_nrs:
            nr_of_matches += 1
    
    if nr_of_matches > 0:
        ans = ans + 2 ** (nr_of_matches-1)
print(ans)