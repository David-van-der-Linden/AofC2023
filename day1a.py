import re
from my_secrets import path

file = open(path + 'input1.txt')

ans = 0
for line in file:
    # get first and last word
    first = re.search("[0-9]", line).group()
    last = re.search("[0-9]", line[::-1]).group()
    
    ans += int(first+last)

print(ans)