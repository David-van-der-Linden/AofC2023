from my_secrets import path
from tqdm import tqdm

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
# seq_to_min_ssl(seq) = '#.##.###'
# len(seq_to_min_ssl(seq)) = sum(seq) + len(seq) - 1
#                      = 6 + 3 - 1 = 8
# if our string of spring labels is
# ssl = '????????',     len(ssl) = 8
# then there is only one way for this seq ssl pair to match
# ssl = '?????????',    len(ssl) = 9
# then balls = len(ssl) - len(seq_to_min_ssl(seq)) = 1
# this is how much leeway we have this leeway can be inserted
# into the shortest sting in one of the following ways
# '.#.##.###', '#..##.###', '#.##..###', '#.##.###.'
# we can look at it if there where cups _ in the shortest sting
# '_#._##._###_' and we can place the balls in the cups

# we can assume without loss of generality (lel i mean implement a parser)
# that all strings of spring labels (ssls) have no . at the start
# since nr_of_ways(ssl,seq) = nr_of_ways('.'+ssl, seq) for all ssl and seq
# and no consecutive .s since they could be replaced by a single .

# whenever we have a ssl that is leading with an # we can truncate since we know that
# the first # is part of the first element of seq

# add a lookup table to store all things once you have computed them to avoid
# calculating the number of ways of some input twice


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


def seq_to_min_ssl(seq: tuple):
    ssl = ''
    for i in seq:
        ssl = ssl + '#'*i + '.'
    return ssl[:-1]


def nr_of_ways(ssl: str, seq: tuple):
    if (ssl, seq) in lookup:
        return lookup[(ssl, seq)]
    elif ssl == '':
        lookup[(ssl, seq)] = 1 if len(seq) == 0 else 0
        return lookup[(ssl, seq)]
    elif ssl[0] == '.':
        lookup[(ssl, seq)] = nr_of_ways(ssl[1:], seq)
        return lookup[(ssl, seq)]
    elif ssl[0] == '?':
        # return nr_of_ways if add ball + nr_of_ways if remove cup
        lookup[(ssl, seq)] = nr_of_ways(ssl[1:], seq) +\
            nr_of_ways('#' + ssl[1:], seq)
        return lookup[(ssl, seq)]
    elif ssl[0] == '#':
        if len(seq) == 0:
            lookup[(ssl, seq)] = 0
            return 0
        else:
            # check if the first part is feasible
            # then continue with shortened sequence
            if (len(ssl) >= seq[0]+1
                    and not is_feasible(ssl[:seq[0]+1], '#'*seq[0]+'.')):
                lookup[(ssl, seq)] = 0
                return 0
            elif (len(ssl) == seq[0]
                  and not is_feasible(ssl[:seq[0]+1], '#'*seq[0])):
                lookup[(ssl, seq)] = 0
                return 0
            elif len(ssl) < seq[0]:
                lookup[(ssl, seq)] = 0
                return 0
            else:
                lookup[(ssl, seq)] = nr_of_ways(ssl[seq[0]+1:], seq[1:])
                return lookup[(ssl, seq)]
    else:
        assert False


global lookup
lookup = dict()

ans = 0
for line in tqdm(lines):
    split_line = line.split()
    temp_str = split_line[0]
    ssl = f'{temp_str}?{temp_str}?{temp_str}?{temp_str}?{temp_str}'
    temp_seq = [int(val) for val in split_line[1].split(',')]
    seq = temp_seq + temp_seq + temp_seq + temp_seq + temp_seq

    ways = nr_of_ways(ssl, tuple(seq))
    ans += ways

print('ans:', ans)
