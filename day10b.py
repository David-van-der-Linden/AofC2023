# for this one i had multiple ideas

# idea 1
# if you follow the loop as if you where walking on it
# then you are bordering the inside and the outside
# iter to you left or to your right will be inside and the other side
# will be the outside
# you can detect what weather you have to use a right or a left
# if you traverse the loop in a fixed direction then finding the
# the top left most element part of your loop, the one next to it
# and the order in which you come across them will be enough to say
# if left is inside or out
# after you have found the direction you can mark every square relative to your 
# position on the curve as inside or outside, be careful to mark 2 cells next to a corner
# using that every empty cell that is next to an inside cell should also be label inside
# you can now find all inside cells
    
# idea 2
# double the grid, pad the outside with empty cells (first row and first column)
# for all cells on the loop mark there counterpart
# new_cords = original_cords*2 + 1
# for all consecutive cells in the loop mark the cell in between them as part of the loop
# cell with cords 0,0 as outside
# mark all adjacent non pipe cells of outside cells as outside
# map back to normal grid_size (or just count directly on larger grid)

# idea 2 seems quicker to implement so lets do that

import re
import numpy as np
from my_secrets import path


with open(path + 'input10.txt') as f:
    lines = f.read().split('\n')

for line_index in range(len(lines)):
    line = lines[line_index]
    col_s = re.search('S', line)
    if col_s:
        col_s = col_s.span()[0]
        row_s = line_index
        break

get_ends = {'|': [[-1,0],[1, 0]],
            '-': [[0,-1],[0,1]],
            'L': [[-1,0],[0,1]],
            'J': [[0,-1],[-1,0]],
            '7': [[0,-1],[1,0]],
            'F': [[1,0],[0,1]]}

def get_next(row_l : int, col_l : int, row_c : int, col_c : int, symbol : str):
    # reruns coordinates of the next symbol along the path
    # or raises error
    last = np.array([row_l, col_l])
    current = np.array([row_c, col_c])

    # idea
    # for symbol get relative positions and check which one already occupied
    ends = get_ends[symbol]
    if (last == current + np.array(ends[0])).all():
        out = current + np.array(ends[1])
        return out[0], out[1]
    elif (last == current + np.array(ends[1])).all():
        out = current + np.array(ends[0])
        return out[0], out[1]
    else:
        raise 'ends not match current and last'

# from looking at the puzzle input we deduced that the start node should be a '-'
# let us chose to start on the right of S and end on the left of S
row_l = row_s
col_l = col_s
row_c = row_s
col_c = col_s + 1

loop_cells = [(row_l, col_l), (row_c, col_c)]
while (row_c, col_c) != (row_s, col_s - 1):   # input
# while (row_c, col_c) != (row_s + 1, col_s):     # test_input
    row_n, col_n = get_next(row_l, col_l, row_c, col_c, lines[row_c][col_c])
    loop_cells.append((row_n, col_n))
    row_l, col_l, row_c, col_c = row_c, col_c, row_n, col_n

# print(loop_cells)
big_grid = [['.' for _ in range(2*len(lines[0])+1)] for _ in range(2*len(lines)+1)]

def old_to_new(cord):
    return 2 * cord + 1

def label_a_and_almost_b(cell_a, cell_b):
    # label cell a in new grid
    big_grid[old_to_new(cell_a[0])][old_to_new(cell_a[1])] = '#'
    # label the cell in between a and b in new grid
    big_grid[int(old_to_new((cell_a[0] + cell_b[0]) / 2))][int(old_to_new((cell_a[1] + cell_b[1]) / 2))] = '#'

for i in range(len(loop_cells)-1):
    cell_a = loop_cells[i]
    cell_b = loop_cells[i+1]
    label_a_and_almost_b(cell_a, cell_b)

# do the same for the last and first
cell_a = loop_cells[-1]
cell_b = loop_cells[0]
label_a_and_almost_b(cell_a, cell_b)

def vis_grid(grid : list[list[str]], path : str):
    grid_str = []
    for row in grid:
        grid_str.append(''.join(row)+'\n')
    grid_str = ''.join(grid_str)
    f = open(path, 'w')
    f.write(grid_str)
    f.close()

directions = {(1, 0), (-1, 0), (0, 1), (0, -1)}

class board():
    def __init__(self, grid):
        self.grid = grid
        
    def color_this_and_touching(self, initial_loc: tuple[int], symbol: str):
        queue = [initial_loc]
        visited = [[False for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        while len(queue) > 0:
            loc = queue.pop(0)
            self.grid[loc[0]][loc[1]] = symbol
            for dir in directions:
                new_loc = (loc[0] + dir[0], loc[1] + dir[1])
                if (0 <= new_loc[0] < len(self.grid[0])) \
                    and (0 <= new_loc[1] < len(self.grid)) \
                    and not visited[new_loc[0]][new_loc[1]] \
                    and self.grid[new_loc[0]][new_loc[1]] == '.':
                    queue.append(new_loc)
                    visited[new_loc[0]][new_loc[1]] = True

    def get_num_odd_sym_in_grid(self, symbol : str):
        num = 0
        for i in range(1, len(self.grid), 2):
            for j in range(1, len(self.grid[0]), 2):
                if self.grid[i][j] == symbol:
                    num += 1
        return num

vis_grid(big_grid, path + 'big_grid_pre_color.txt')
my_object = board(big_grid)
my_object.color_this_and_touching((0, 0), 'O')
vis_grid(my_object.grid, path + 'big_grid_vised.txt')
print('ans:', my_object.get_num_odd_sym_in_grid('.'))
