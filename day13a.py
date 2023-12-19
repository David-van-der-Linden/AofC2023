from my_secrets import path
from math import floor
from math import ceil

with open(path + 'input13.txt') as f:
    patterns = f.read().split('\n\n')


def get_row_mirrors(lines: list):
    to_return = []
    # idea try all possible mirror locations and check
    # if whats to the left of the mirror is the same as to the right of the mirror (but mirrored)

    # first half
    for mirror_index in range(1, floor(len(lines)/2)+1):
        lhs = lines[:mirror_index]
        rhs = lines[mirror_index:(mirror_index*2)][::-1]
        assert len(lhs) == len(rhs)
        if lhs == rhs:
            to_return.append(mirror_index)

    # middle (if it exists)
    if floor(len(lines)/2) != ceil(len(lines)/2):
        mirror_index = floor(len(lines)/2)+1
        # same but pop first element of left list
        lhs = lines[1:mirror_index]
        rhs = lines[mirror_index:][::-1]
        assert len(lhs) == len(rhs)
        if lhs == rhs:
            to_return.append(mirror_index)

    # last half
    for mirror_index in range(ceil(len(lines)/2)+1, len(lines)):
        # reversed index is the mirrored index but counting from the right instead
        reversed_index = len(lines)-mirror_index
        lhs = lines[(mirror_index-reversed_index):mirror_index]
        rhs = lines[mirror_index:][::-1]
        if lhs == rhs:
            to_return.append(mirror_index)

    return to_return


def get_col_mirrors(lines: list):
    # transpose
    t_lines = [''.join(s) for s in zip(*lines)]
    return get_row_mirrors(t_lines)


ans = 0
for pattern in patterns:
    lines = pattern.split('\n')
    rows = get_row_mirrors(lines)
    cols = get_col_mirrors(lines)
    ans += 100 * sum(rows)
    ans += sum(cols)
print(ans)
