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

    flag = True
    for i in range(len(pattern)):
        # since we are dealing with mirrors we can get away with ony replacing # by .
        # since if we need to replace a . by a # then we can also do the opposite in the reflection
        if pattern[i] == '#':
            new_pattern = pattern[:i] + '.' + pattern[(i+1):]
            new_lines = new_pattern.split('\n')
            new_rows = get_row_mirrors(new_lines)
            new_cols = get_col_mirrors(new_lines)

            # get rid of the old reflection if its there
            for row in rows:
                if row in new_rows:
                    new_rows.remove(row)
            for col in cols:
                if col in new_cols:
                    new_cols.remove(col)

            if sum(new_rows)+sum(new_cols) != 0:
                # then we have found the pattern with the smudge
                ans += 100*sum(new_rows)+sum(new_cols)
                continue
print(ans)
