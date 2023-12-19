from my_secrets import path

with open(path + 'input9.txt') as f:
    lines = f.read().split('\n')


def get_diff(line: list):
    difference_row = []
    for value_index in range(1, len(line)):
        difference_row.append(line[value_index]-line[value_index - 1])
    return difference_row

# idea carry out the steps like described in the question
# only store the last element of a difference row (since the rest is not needed for finding answer)


ans = 0
for line in lines:
    line = [int(val) for val in line.split()]
    ends = [line[-1]]
    diff = get_diff(line)
    while diff != [0 for _ in range(len(diff))]:
        ends.append(diff[-1])
        diff = get_diff(diff)
    next_in_seq = sum(ends)
    ans += next_in_seq

print(ans)
