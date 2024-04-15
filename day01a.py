import re
from my_secrets import path

with open(path + 'input1.txt') as f:
    lines = f.read().split('\n')

ans = 0
for line in lines:
    # get first and last word
    first = re.search("[0-9]", line).group()
    last = re.search("[0-9]", line[::-1]).group()

    ans += int(first+last)

print(ans)
