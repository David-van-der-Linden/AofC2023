from my_secrets import path

with open(path + 'input15.txt') as f:
    steps = f.read().split(',')


def get_hash(step):
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value


ans = 0
for step in steps:
    ans += get_hash(step)

print(ans)
