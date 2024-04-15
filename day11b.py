from my_secrets import path

with open(path + 'input11.txt') as f:
    lines = f.read().split('\n')


def get_empty_rows(lines):
    """Entry is 1 if a corresponding row has no stars and 0 otherwise."""
    empty_rows = [0 for _ in range(len(lines))]
    for line_index in range(len(lines)):
        line = lines[line_index]
        if line == '.'*len(line):
            empty_rows[line_index] = 1
    return empty_rows


def get_empty_cols(lines):
    """Entry is 1 if a corresponding col has no stars and 0 otherwise."""
    transposed_lines = [''.join(s) for s in zip(*lines)]
    return get_empty_rows(transposed_lines)


def dst(a, b):
    extra_row_dist = sum(
        empty_rows[min(a[0], b[0]):max(a[0], b[0])])*(1000000-1)
    extra_col_dist = sum(
        empty_cols[min(a[1], b[1]):max(a[1], b[1])])*(1000000-1)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + extra_row_dist + extra_col_dist


stars = set()
for line_index in range(len(lines)):
    line = lines[line_index]
    for column_index in range(len(line)):
        if lines[line_index][column_index] == '#':
            stars.add((line_index, column_index))

empty_rows = get_empty_rows(lines)
empty_cols = get_empty_cols(lines)

# compute dist a to b for all combinations of a != b
# this counts both a b and b a
double_dist = 0
for star_a in stars:
    for star_b in stars:
        if star_a == star_b:
            continue
        else:
            double_dist += dst(star_a, star_b)

total_dist = double_dist / 2
print(int(total_dist))
