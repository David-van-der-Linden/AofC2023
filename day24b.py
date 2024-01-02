from my_secrets import path
from sympy import symbols, Eq, solve
import re

with open(path + 'input24.txt') as f:
    lines = f.read().split('\n')

x = list()
v = list()
for i, line in enumerate(lines):
    xv = [int(num) for num in re.split(',[ ]*| @ ', line)]
    x.append(tuple(xv[:3]))
    v.append(tuple(xv[3:]))

# idea new hailstone is xn vn
# xn + ti * vn = xi + ti * vi for all i
# where ti ti in \mathbb{R} is time of collision
# when having 4 lines and picking a 5th line
# to intersect with all of them
# assuming some conditions line lines not being parallel and all lines being distinct
# we know that the 5th line intersecting with all of them is uniquely defined
# and finding the ti's for the lines can be done after finding the lines and can be done with only 3 lines
# therefor we only need the first 4 hailstones of the input to find xn
# just to be sure lets take 5 hailstones
# since this is a small number of variables we can use a solver 
# to solve this system of equations quickly

xns = symbols('xn0:%d' % 3)
vns = symbols('vn0:%d' % 3)
ts = symbols('t0:%d' % 5)

system = tuple()
for i in range(4):
    # xn + ti * vn = xi + ti * vi
    for dim in range(3):
        system = system + \
            (Eq(xns[dim] + ts[i] * vns[dim], x[i][dim] + ts[i] * v[i][dim]),)

variables = xns + vns + ts
print('variables\n', variables)
solutions = solve(system, variables)
print("Solutions:")
print(solutions)
assert len(solutions) == 1
for solution in solutions:
    ans = solution[0] + solution[1] + solution[2]
    print('ans', ans)