import re
from turtle import distance
from my_secrets import path

with open(path + 'input11.txt') as f:
    lines = f.read().split('\n')


def get_empty_rows(lines):
    # entry is 1 if a corresponding row has no stars and 0 otherwise
    empty_rows = [0 for _ in range(len(lines))]
    for line_index in range(len(lines)):
        line = lines[line_index]
        if line == '.'*len(line):
            empty_rows[line_index] = 1
    return empty_rows


def get_empty_cols(lines):
    # entry is 1 if a corresponding col has no stars and 0 otherwise
    transposed_lines = [''.join(s) for s in zip(*lines)]
    return get_empty_rows(transposed_lines)


def dst(A, B):
    extra_row_dist = sum(
        empty_rows[min(A[0], B[0]):max(A[0], B[0])])*(1000000-1)
    extra_col_dist = sum(
        empty_cols[min(A[1], B[1]):max(A[1], B[1])])*(1000000-1)
    return abs(A[0] - B[0]) + abs(A[1] - B[1]) + extra_row_dist + extra_col_dist


stars = set()
for line_index in range(len(lines)):
    line = lines[line_index]
    for column_index in range(len(line)):
        if lines[line_index][column_index] == '#':
            stars.add((line_index, column_index))

global empty_rows
global empty_cols
empty_rows = get_empty_rows(lines)
empty_cols = get_empty_cols(lines)

# compute dist A to B for all combinations of A != B
# this counts both A B and B A
double_dist = 0
for star_A in stars:
    for star_B in stars:
        if star_A == star_B:
            continue
        else:
            double_dist += dst(star_A, star_B)

total_dist = double_dist / 2
print(int(total_dist))
