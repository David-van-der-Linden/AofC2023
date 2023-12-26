from my_secrets import path
from copy import deepcopy
from tqdm import tqdm
import itertools as it

with open(path + 'input14.txt') as f:
    lines = f.read().split('\n')


def list_to_tuple(*args):
    return tuple(args)

class dish_obj():
    def __init__(self, lines):
        self.dish = [list(row) for row in lines]

    def up_color_since_last_ht(self, last_ht, O_count, j):
        for filler_i in range(last_ht + 1, last_ht + 1 + O_count):
            self.dish[filler_i][j] = 'O'

    def move_col_up(self, j):
        O_count = 0
        last_ht = -1
        for scanner_i, _ in enumerate(self.dish):
            if self.dish[scanner_i][j] == 'O':
                O_count += 1
                self.dish[scanner_i][j] = '.'
            elif self.dish[scanner_i][j] == '#':
                self.up_color_since_last_ht(last_ht, O_count, j)
                last_ht = scanner_i
                O_count = 0
        self.up_color_since_last_ht(last_ht, O_count, j)

    def move_all_up(self):
        for j in range(len(self.dish[0])):
            self.move_col_up(j)

    def down_color_since_last_ht(self, last_ht, O_count, j):
        for filler_i in range(last_ht - 1, last_ht - 1 - O_count, -1):
            self.dish[filler_i][j] = 'O'

    def move_col_down(self, j):
        O_count = 0
        last_ht = len(self.dish)
        for scanner_i, _ in reversed(list(enumerate(self.dish))):
            if self.dish[scanner_i][j] == 'O':
                O_count += 1
                self.dish[scanner_i][j] = '.'
            elif self.dish[scanner_i][j] == '#':
                self.down_color_since_last_ht(last_ht, O_count, j)
                last_ht = scanner_i
                O_count = 0
        self.down_color_since_last_ht(last_ht, O_count, j)

    def move_all_down(self):
        for j in range(len(self.dish[0])):
            self.move_col_down(j)

    def left_color_since_last_ht(self, last_ht, O_count, i):
        for filler_j in range(last_ht + 1, last_ht + 1 + O_count):
            self.dish[i][filler_j] = 'O'

    def move_col_left(self, i):
        O_count = 0
        last_ht = -1
        for scanner_j, _ in enumerate(self.dish[0]):
            if self.dish[i][scanner_j] == 'O':
                O_count += 1
                self.dish[i][scanner_j] = '.'
            elif self.dish[i][scanner_j] == '#':
                self.left_color_since_last_ht(last_ht, O_count, i)
                last_ht = scanner_j
                O_count = 0
        self.left_color_since_last_ht(last_ht, O_count, i)

    def move_all_left(self):
        for i in range(len(self.dish)):
            self.move_col_left(i)

    def right_color_since_last_ht(self, last_ht, O_count, i):
        for filler_j in range(last_ht - 1, last_ht - 1 - O_count, -1):
            self.dish[i][filler_j] = 'O'

    def move_col_right(self, i):
        O_count = 0
        last_ht = len(self.dish[0])
        for scanner_j, _ in reversed(list(enumerate(self.dish[0]))):
            if self.dish[i][scanner_j] == 'O':
                O_count += 1
                self.dish[i][scanner_j] = '.'
            elif self.dish[i][scanner_j] == '#':
                self.right_color_since_last_ht(last_ht, O_count, i)
                last_ht = scanner_j
                O_count = 0
        self.right_color_since_last_ht(last_ht, O_count, i)

    def move_all_right(self):
        for i in range(len(self.dish)):
            self.move_col_right(i)

    def do_cycle(self):
        self.move_all_up()
        self.move_all_left()
        self.move_all_down()
        self.move_all_right()

    def visualize(self):
        for line in self.dish:
            print(''.join(line))

states = dict()
obj = dish_obj(lines)
first_map_to = -1
for cycle_nr in tqdm(range(1000000000)):
    # print('\ncycle_nr', cycle_nr)
    # obj.visualize()
    tup = tuple(it.starmap(list_to_tuple, obj.dish))
    if tup in states:
        # print(f' {cycle_nr} maps to {states[tup]}')
        if first_map_to == -1:
            first_map_to = states[tup]
            first_map_from = cycle_nr
        elif states[tup] == first_map_to:
            second_map_from = cycle_nr
            break
    else:
        states[tuple(it.starmap(list_to_tuple, deepcopy(obj.dish)))] = cycle_nr
    obj.do_cycle()

# we see the following pattern emerge for the test set
# for i in range(20):
#     print(f'{i} to {((i - 3) % 7) + 3}')
# we in general that would be
# for i in range(20):
#     print(f'{i} to {((i - first_map_from) % (second_map_from - first_map_from)) + first_map_to}')
# so map 1000000000 is the same as
map_nr = ((1000000000 - first_map_from) % (second_map_from - first_map_from)) + first_map_to
# the easiest is to just run again from the start for map_nr many iterations
new_obj = dish_obj(lines)
for cycle_nr in tqdm(range(map_nr)):
	new_obj.do_cycle()

ans = 0
for row_index, row in enumerate(new_obj.dish):
    row_weight = len(new_obj.dish) - row_index
    for char in row:
        if char == 'O':
            ans += row_weight
print('ans', ans)
