import math
import re
from my_secrets import path

with open(path + 'input6.txt') as f:
    lines = f.read().split('\n')

Ts  = [int(T) for T in re.findall('[0-9]+',lines[0])]
recs = [int(rec) for rec in re.findall('[0-9]+',lines[1])]

# So i did the math

# t = time_held
# T = time_available
# rec = record_time
# dist = distance_traveled

# dist = (T-t)t = Tt-tt
# winning means dist > rec
# which is equitant to
# dist - (rec + 1) >= 0
# Tt - tt - (rec + 1) >= 0
# t^2 -Tt + (rec + 1) <= 0
# by quadratic rule (abc formula) this is zero when
# t = (T +- sqrt(T^2 - 4 * (rec + 1)))/2
# since its a second order function with negative second order coefficient
# we will need to round up to get the values of te we are looking for

# we further should watch out if T^2 - 4 * (rec + 1) <0

prod = 1
for i in range(len(Ts)):
    T = Ts[i]
    rec = recs[i]
    assert T ** 2 - 4 * (rec + 1) >= 0
    t_min = math.ceil(T/2 - 1/2* math.sqrt(T**2-4*(rec+1)))
    t_max = math.floor(T/2 + 1/2* math.sqrt(T**2-4*(rec+1)))
    ways = t_max - t_min + 1
    prod = prod * ways

    print('t_min', t_min)
    print('t_max', t_max)
    print('ways', ways)

print('prod', prod)
