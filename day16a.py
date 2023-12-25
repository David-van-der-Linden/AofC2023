import numpy as np
from tqdm import tqdm
from my_secrets import path

with open(path + 'input16.txt') as f:
    lines = f.read().split('\n')

# idea simulate moving of all beams step by step as described in exercise
# store a beam as (row, column, direction)
# keep track of all states beams have been in
# remove a beam when it is in a state that has already been visited
# remove beams that are off the board
# run till list of beams is empty

dir_to_cords = {'R': (0, 1),
                'L': (0, -1),
                'U': (-1, 0),
                'D': (1, 0)}

# /
dir_to_slash = {'R': 'U',
                'L': 'D',
                'U': 'R',
                'D': 'L'}

# \
dir_to_back_slash = {'R': 'D',
                     'L': 'U',
                     'U': 'L',
                     'D': 'R'}


class laser_board():
    def __init__(self, lines):
        self.lines = lines
        self.beams = [(0, 0, 'R')]
        self.energized = np.array(
            [[False for _ in range(len(lines[0]))]
             for _ in range(len(lines))])
        self.visited = set()

    def move(self):
        to_pop = []
        to_append = []
        for beam_index, beam in enumerate(self.beams):
            if not (0 <= beam[0] <= len(self.lines)-1 and
                    0 <= beam[1] <= len(self.lines[0])-1):
                to_pop.append(beam_index)
            elif beam in self.visited:
                to_pop.append(beam_index)
            else:
                self.energized[beam[0]][beam[1]] = True
                self.visited.add(beam)
                if self.lines[beam[0]][beam[1]] == '.':
                    self.move_this_beam_straight(beam_index)
                elif self.lines[beam[0]][beam[1]] == '|':
                    if beam[2] == 'R' or beam[2] == 'L':
                        to_append.append((beam[0] + 1, beam[1], 'D'))
                        to_append.append((beam[0] - 1, beam[1], 'U'))
                        to_pop.append(beam_index)
                    else:
                        self.move_this_beam_straight(beam_index)
                elif self.lines[beam[0]][beam[1]] == '-':
                    if beam[2] == 'U' or beam[2] == 'D':
                        to_append.append((beam[0], beam[1] + 1, 'R'))
                        to_append.append((beam[0], beam[1] - 1, 'L'))
                        to_pop.append(beam_index)
                    else:
                        self.move_this_beam_straight(beam_index)
                elif self.lines[beam[0]][beam[1]] == '/':
                    self.beams[beam_index] = (beam[0],
                                              beam[1],
                                              dir_to_slash[beam[2]])
                    self.move_this_beam_straight(beam_index)
                elif self.lines[beam[0]][beam[1]] == '\\':
                    self.beams[beam_index] = (beam[0],
                                              beam[1],
                                              dir_to_back_slash[beam[2]])
                    self.move_this_beam_straight(beam_index)
                else:
                    assert False
        self.beams.extend(to_append)
        assert to_pop == sorted(to_pop)
        for i in reversed(to_pop):
            self.beams.pop(i)

    def move_this_beam_straight(self, beam_index):
        beam = self.beams[beam_index]
        self.beams[beam_index] = (beam[0] + dir_to_cords[beam[2]][0],
                                  beam[1] + dir_to_cords[beam[2]][1],
                                  beam[2])

obj = laser_board(lines)
while len(obj.beams) > 0:
    obj.move()

ans = 0
for i in range(len(obj.energized)):
    for j in range(len(obj.energized[0])):
        if obj.energized[i][j]:
            ans += 1
print('ans', ans)
