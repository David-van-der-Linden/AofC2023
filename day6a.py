import math
import re
from my_secrets import path

with open(path + 'input6.txt') as f:
    lines = f.read().split('\n')

Ts  = [int(T) for T in re.findall('[0-9]+',lines[0])]
recs = [int(rec) for rec in re.findall('[0-9]+',lines[1])]

prod = 1
for i in range(len(Ts)):
    T = Ts[i]
    rec = recs[i]
    t_min = math.ceil(T/2 - 1/2* math.sqrt(T**2-4*(rec+1)))
    print('t_min', t_min)
    t_max = math.floor(T/2 + 1/2* math.sqrt(T**2-4*(rec+1)))
    print('t_max', t_max)
    ways = t_max - t_min + 1
    print('ways', ways)
    prod = prod * ways

print('prod', prod)
