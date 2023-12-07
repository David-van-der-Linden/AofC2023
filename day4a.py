import re
from my_secrets import path

with open(path + 'input4.txt') as f:
    lines = f.read().split('\n')

ans = 0
for line in lines:
    # print(line)
    split_line = line.split(':')[1]
    split_line = split_line.split('|')
    #  print(split_line)

    winning_numbers = re.findall('[0-9]+', split_line[0])
    numbers_on_card = re.findall('[0-9]+', split_line[1])
    # print('winning_numbers', winning_numbers)
    # print('numbers_on_card', numbers_on_card)

    nr_of_matches = 0
    for nr in numbers_on_card:
        if nr in winning_numbers:
            # print(nr)
            nr_of_matches += 1
    
    if nr_of_matches > 0:
        ans = ans + 2 ** (nr_of_matches-1)
    # print('nrofmachtes', nr_of_matches)
    # print(2 ^ (nr_of_matches-1))
    # print('ansthus far', ans)
print(ans)