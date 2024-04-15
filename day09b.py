from my_secrets import path

with open(path + 'input9.txt') as f:
    lines = f.read().split('\n')


def get_diff(split_line: list):
    difference_row = []
    for value_index in range(1, len(split_line)):
        difference_row.append(split_line[value_index]-split_line[value_index - 1])
    return difference_row

# idea is similar to the first question however we need to
# store the first entry of each difference row instead


ans = 0
for line in lines:
    split_line = [int(val) for val in line.split()]
    front_ends = [split_line[0]]
    diff = get_diff(split_line)
    while diff != [0 for _ in range(len(diff))]:
        front_ends.append(diff[0])
        diff = get_diff(diff)

    next_in_seq = 0
    for front_end in reversed(front_ends):
        next_in_seq = front_end - next_in_seq
    ans += next_in_seq

print(ans)
