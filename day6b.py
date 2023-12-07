import math
import re
from my_secrets import path

with open(path + 'input6.txt') as f:
    lines = f.read().split('\n')



T = 52947594
rec = 426137412791216
t_min = math.ceil(T/2 - 1/2* math.sqrt(T**2-4*(rec+1)))
print('t_min', t_min)
t_max = math.floor(T/2 + 1/2* math.sqrt(T**2-4*(rec+1)))
print('t_max', t_max)
ways = t_max - t_min + 1
print('ways', ways)

