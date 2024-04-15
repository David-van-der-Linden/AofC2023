import re
from tqdm import tqdm
from my_secrets import path

with open(path + 'input12.txt') as f:
    lines = f.read().split('\n')

# idea brute force all possible combinations and count the ones that work
# needed:
# 1. A way to convert string of .'s and #'s to the corresponding sequence of numbers
# 2. A way of turning string of .'s, #'s, and ?'s into all possible strings
# where ?'s are replaced by .'s and #'s
# 3. A way of counting all the correct strings

# 1


def compute_seq(input_str: str) -> list[int]:
    """Returns sequence in list form '#.#.###' -> [1, 1, 3].\n
    The size of each contiguous group of damaged springs,\n
    is listed in the order those groups appear in the row."""
    return [len(temp_str) for temp_str in re.findall('#+', input_str)]

# 2


def get_all_str(input_list: list[str]) -> list[str]:
    """Input list of string containing ?'s.\n
    Returns list of all possible strings not containing ?'s.\n
    So all ? are replaced by either a . or a #"""

    to_return = []
    for og_str in input_list:
        question_index = og_str.find('?')
        # if no hit
        if question_index == -1:
            # then schedule this string for return
            to_return.append(og_str)
        else:
            # replace one character at the time and iterate
            to_return.extend(get_all_str(\
                [og_str[:question_index]+'.'+og_str[(question_index+1):]]))
            to_return.extend(get_all_str(\
                [og_str[:question_index]+'#'+og_str[(question_index+1):]]))
    return to_return


# 3
ans = 0
for line in tqdm(lines):
    split_line = line.split()
    input_str = split_line[0]
    desired_seq = [int(val) for val in split_line[1].split(',')]

    ways = 0
    for brute_sting in get_all_str(input_list=[input_str]):
        if compute_seq(brute_sting) == desired_seq:
            ways += 1
    ans += ways

print('ans:', ans)
