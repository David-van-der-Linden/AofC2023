from my_secrets import path

with open(path + 'input9.txt') as f:
    lines = f.read().split('\n')

def get_diff(line : list):
    difference_row = []
    for value_index in range(1, len(line)):
        difference_row.append(line[value_index]-line[value_index - 1])
    return difference_row

# idea is similar to the first question however we need to 
# store the first entry of each difference row instead

ans = 0
for line in lines:
    line = [int(val) for val in line.split()]
    front_ends = [line[0]]
    diff = get_diff(line)
    while diff != [0 for _ in range(len(diff))]:
        front_ends.append(diff[0])
        diff = get_diff(diff)
    
    next_in_seq = 0
    for front_end in reversed(front_ends):
        next_in_seq =  front_end - next_in_seq
    ans += next_in_seq

print(ans)