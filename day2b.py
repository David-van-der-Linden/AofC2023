import re
import numpy as np
from my_secrets import path

with open(path + 'input2.txt') as f:
    lines = f.read().split('\n')

ans=0

for line_index in range(len(lines)):
    line = lines[line_index]

    my_dict = {'red':0,
            'green':0,
            'blue':0}

    def my_def():
        split_line = line.split(':')[1]
        draws = split_line.split(';')
        # print(draws)
        for draw in draws:
            split_draw = draw.split(',')
            # print('split_draw:', split_draw)
            for ball in split_draw:
                split_ball = ball.split(' ')
                # print('split_ball', split_ball)
                nr = int(split_ball[1])
                color = split_ball[2]
                if nr > my_dict[color]:
                    my_dict[color] = nr
        
        print('my_dict', my_dict)
        power = 1
        for color in my_dict:
            power = power * my_dict[color]
        print('power', power)
        return power
    
    ans += my_def()

print(ans)