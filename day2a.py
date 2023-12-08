import re
import numpy as np
from my_secrets import path

with open(path + 'input2.txt') as f:
    lines = f.read().split('\n')

my_dict = {'red':12,
           'green':13,
           'blue':14}

ans=0

for line_index in range(len(lines)):
    line = lines[line_index]
    def my_def():
        split_line = line.split(':')[1]
        draws = split_line.split(';')
        for draw in draws:
            split_draw = draw.split(',')
            for ball in split_draw:
                split_ball = ball.split(' ')
                nr = int(split_ball[1])
                color = split_ball[2]
                # if greater that specified by exercise complain
                if nr > my_dict[color]:
                    return False
        return True
    
    if my_def():
        ans += line_index+1

print(ans)