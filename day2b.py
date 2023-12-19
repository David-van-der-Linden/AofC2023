import re
import numpy as np
from my_secrets import path

with open(path + 'input2.txt') as f:
    lines = f.read().split('\n')

ans = 0

for line_index in range(len(lines)):
    line = lines[line_index]

    my_dict = {'red': 0,
               'green': 0,
               'blue': 0}

    def my_def():
        split_line = line.split(':')[1]
        draws = split_line.split(';')
        for draw in draws:
            split_draw = draw.split(',')
            for ball in split_draw:
                split_ball = ball.split(' ')
                nr = int(split_ball[1])
                color = split_ball[2]
                # update my_dict to have the maximum occurring color
                if nr > my_dict[color]:
                    my_dict[color] = nr

        # compute power
        power = 1
        for color in my_dict:
            power = power * my_dict[color]
        print('power', power)
        return power

    ans += my_def()

print(ans)
