from my_secrets import path
from collections import Counter

input_file = 'input7.txt'

# compare hands
# print('143'>='123')
# if we map capital letters to lowercase letters we can use string comparison for which hand wins given there the same type
cap_to_lower = {'A': 'z',
                'K': 'y',
                'Q': 'x',
                'J': 'w',
                'T': 'v'}

# idea parse all replace letters according to cap_to_lower
# add a symbol at the start indicating which hand type it is and then apply a sorting algorithm to it


def determine_type(hand: str) -> str:
    """Input hand is a string of length 5.\n
    Returns single character string between a and g,\n
    where g corresponds to the best hand type and a to the worst hand type.
    """

    # a_val is how often the most occurring character occurs
    # Counter(hand) is dictionary that counts how often a character occurs in a string
    a_val = max(Counter(hand).values())
    # b_val is how often the second most occurring character occurs
    if a_val != 5:
        b_val = sorted(Counter(hand).values())[-2]

    # logic for determining which hand type we have
    if a_val == 5:
        # type 5 of a kind
        return 'g'
    elif a_val == 4:
        # type 4 of a kind
        return 'f'
    elif a_val == 3 and b_val == 2:
        # type full house
        return 'e'
    elif a_val == 3:
        # type 3 of a kind
        return 'd'
    elif a_val == 2 and b_val == 2:
        # type 2 pair
        return 'c'
    elif a_val == 2:
        # type 1 pair
        return 'b'
    else:
        # type high card
        return 'a'


with open(path + input_file) as f:
    file = f.read()

    # replace high cards to match string comparison
    for key in cap_to_lower:
        file = file.replace(key, cap_to_lower[key])

    lines = file.split('\n')

# add hand type symbol at start
for i in range(len(lines)):
    lines[i] = determine_type(lines[i].split()[0]) + lines[i]

lines.sort()

ans = 0
for count, line in enumerate(lines):
    rank = count + 1
    bet = int(line.split()[1])
    ans += rank*bet

print(ans)
