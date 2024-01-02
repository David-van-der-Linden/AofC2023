from __future__ import division
from my_secrets import path
import re

# line intersection code by rook
# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines


def make_line(p1, v1):
    p2 = (p1[0] + v1[0], p1[1] + v1[1])
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False

with open(path + 'input24.txt') as f:
    lines = f.read().split('\n')

x = list()
v = list()
for i, line in enumerate(lines):
    xv = [int(num) for num in re.split(',[ ]*| @ ', line)]
    x.append(tuple(xv[:2]))
    v.append(tuple(xv[3:-1]))

bound_min = 200000000000000
bound_max = 400000000000000
# bound_min = 7
# bound_max = 27

ans = 0
for stone1 in range(len(lines)-1):
    for stone2 in range(stone1 + 1, len(lines)):
        L1 = make_line(x[stone1], v[stone1])
        L2 = make_line(x[stone2], v[stone2])
        R = intersection(L1, L2)
        if R:
            # print("Intersection detected:", R)
            # check if intersection in bounding box
            if bound_min <= R[0] <= bound_max and bound_min <= R[1] <= bound_max:
                # to check for if its in the future
                # # if v[stone1][i] > 0 then
                # # only add if R[0] > x[stone1][i]
                # # if v[stone1][i] < 0 then
                # # only add if R[0] < x[stone1][i]

                # check stone 1
                for i in range(2):
                    if v[stone1][i] != 0:
                        if v[stone1][i] > 0:
                            flag = (R[i] > x[stone1][i])
                            break
                        elif v[stone1][i] < 0:
                            flag = (R[i] < x[stone1][i])
                            break
                        else:
                            assert False
                else:
                    assert False
                # check stone 2
                if flag:
                    for i in range(2):
                        if v[stone2][i] != 0:
                            if v[stone2][i] > 0:
                                ans += 1 if R[i] > x[stone2][i] else 0
                                break
                            elif v[stone2][i] < 0:
                                ans += 1 if R[i] < x[stone2][i] else 0
                                break
                            else:
                                assert False
                    else:
                        assert False
        else:
            # print("No single intersection point detected")
            pass
print('ans', ans)
