from my_secrets import path

with open(path + 'input9.txt') as f:
    lines = f.read().split('\n')


def get_diff(split_line: list[int]):
    difference_row = []
    for value_index in range(1, len(split_line)):
        difference_row.append(split_line[value_index]-split_line[value_index - 1])
    return difference_row

# idea carry out the steps like described in the question
# only store the last element of a difference row (since the rest is not needed for finding answer)


ans = 0
for line in lines:
    split_line = [int(val) for val in line.split()]
    ends = [split_line[-1]]
    diff = get_diff(split_line)
    while diff != [0 for _ in range(len(diff))]:
        ends.append(diff[-1])
        diff = get_diff(diff)
    next_in_seq = sum(ends)
    ans += next_in_seq

print(ans)
