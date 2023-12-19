import math

# same math just only one input this time

T = 52947594
rec = 426137412791216
assert T ** 2 - 4 * (rec + 1) >= 0
t_min = math.ceil(T/2 - 1/2 * math.sqrt(T**2-4*(rec+1)))
t_max = math.floor(T/2 + 1/2 * math.sqrt(T**2-4*(rec+1)))
ways = t_max - t_min + 1

print('t_min', t_min)
print('t_max', t_max)
print('ways', ways)
