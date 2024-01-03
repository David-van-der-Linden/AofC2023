import re
from my_secrets import path

file = open(path + 'input1.txt')

word_to_num = {'zero': '0',
               'one': '1',
               'two': '2',
               'three': '3',
               'four': '4',
               'five': '5',
               'six': '6',
               'seven': '7',
               'eight': '8',
               'nine': '9'}

ans = 0
for line in file:
    # get first and last word
    first = re.search("[0-9]|zero|one|two|three|four|five|six|seven|eight|nine", line).group()
    last = re.search("[0-9]|orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin", line[::-1]).group()
    last = last[::-1]

    # convert to [0-9]
    if first in word_to_num:
        first = word_to_num[first]
    if last in word_to_num:
        last = word_to_num[last]

    ans += int(first+last)

print(ans)
