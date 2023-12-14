from my_secrets import path
import re

with open(path + 'input12.txt') as f:
    lines = f.read().split('\n')

# idea go from right to left
# using cups and balls
# on every iteration iteration add a ball
# or remove a cup
# if there are no balls left then there is only one way
# if there are no cups then there are 0 ways
# implement this recursively to find the number of ways

# lets say we have a sequence
# seq = [1,2,3]
# then the shortest string matching it would be
# sorest_str[seq] = '#.##.###'
# len(sorest_str[seq]) = sum(seq) + len(seq) - 1
#                      = 6 + 3 - 1 = 8
# if our string of spring labels is
# ssl = '????????',     len(ssl) = 8
# then there is only one way for this seq ssl pair to match
# ssl = '?????????',    len(ssl) = 9
# then balls = len(ssl) - len(sorest_str[seq]) = 1
# this is how much leeway we have this leeway can be inserted
# into the shortest sting in one of the following ways
# '.#.##.###', '#..##.###', '#.##..###', '#.##.###.'
# we can look at it if there where cups _ in the shortest sting
# '_#._##._###_' and we can place the balls in the cups

# we can assume without loss of generality (lel i mean implement a parser)
# that all strings of spring labels (ssls) have no . at the start 
# since nr_of_ways(ssl,seq) = nr_of_ways('.'+ssl, seq) for all ssl and seq
# and no consecutive .s since they could be replaced by a single .

def is_feasible(str_with_q, str_without_q):
    # example
    # is_feasible('#.?..#', '#....#') -> True
    # is_feasible('#.?..#', '#...##') -> False
    if len(str_with_q) != len(str_without_q):
        return False
    for i in range(len(str_with_q)):
        char = str_with_q[i]
        if char == '?':
            continue
        elif char != str_without_q[i]:
            return False
    return True

def nr_of_ways(ssl : str, seq : list):
    if ssl == '':
        return 1 if seq == [] else 0
    elif ssl[0] == '.':
        return nr_of_ways(ssl[1:], seq)
    elif ssl[0] == '?':
        # return nr_of_ways if add ball + nr_of_ways if remove cup
        return nr_of_ways(ssl[1:], seq) + nr_of_ways('#' + ssl[1:], seq)
    elif ssl[0] == '#':
        if seq == []:
            return 0
        else:
            # check if the first part is feasible
            # then continue with shortened sequence
            if (len(ssl) >= seq[0]+1
                and not is_feasible(ssl[:seq[0]+1],'#'*seq[0]+'.')):
                return 0
            elif (len(ssl) == seq[0]
                and not is_feasible(ssl[:seq[0]+1],'#'*seq[0])):
                return 0
            elif len(ssl) < seq[0]:
                return 0
            else:
                return nr_of_ways(ssl[seq[0]+1:],seq[1:])
    else:
        assert False 

# ans = 0
# for line in lines:
#     split_line = line.split()
#     temp_str = split_line[0]
#     ssl = f'{temp_str}?{temp_str}?{temp_str}?{temp_str}?{temp_str}'
#     temp_seq = [int(val) for val in split_line[1].split(',')]
#     seq = temp_seq + temp_seq + temp_seq + temp_seq + temp_seq
    
#     print('line', line)
#     print('ssl', ssl)
#     print('seq', seq)
    
#     ways = nr_of_ways(ssl,seq)
#     ans += ways

#     print('ways', ways)

# print('ans:', ans)

# 322650 is to low
print(nr_of_ways('???????#??????##.?'*2+'???????#??????##.', [1,3,2,1,2,1,3,2,1,2,1,3,2,1,2]))
# line ???????#??????##. 1,3,2,1,2
# ssl = '???????#??????##.????????#??????##.????????#??????##.????????#??????##.????????#??????##.'
# seq = [1, 3, 2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 2, 1, 2]