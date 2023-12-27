from my_secrets import path
from tqdm import tqdm
import re

with open(path + 'input22.txt') as f:
    lines = f.read().split('\n')

# idea sort all the bricks by there lowest z value
# then iterate over all the bricks starting with the lowest z value
# drop them down until they hit another brick
# do this by keeping track of the highest dropped point so far for every xy
# and then placing it on top of that instantly

# idea part 2
# drop all
# remove a brick
# drop again while counting how many bricks move


class SandStack():
    def __init__(self, lines):
        self.lines = lines
        self.bricks = list()
        for line_index, line in enumerate(lines):
            self.bricks.append(Brick(line, line_index))

    def drop_all_bricks(self):
        max_x = max(self.bricks, key=lambda x: x.x_high).x_high
        max_y = max(self.bricks, key=lambda x: x.y_high).y_high
        current_top_z = [
            [0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        current_top_brick = [
            ['the ground' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        self.bricks.sort(key=lambda x: x.z_low)
        number_of_bricks_moved = 0
        for i, brick in enumerate(self.bricks):
            top_z = 0
            top_bricks = set()
            for x in range(brick.x_low, brick.x_high + 1):
                for y in range(brick.y_low, brick.y_high + 1):
                    if top_z < current_top_z[x][y]:
                        top_z = current_top_z[x][y]
                        top_bricks.clear()
                        top_bricks.add(current_top_brick[x][y])
                    elif top_z == current_top_z[x][y]:
                        top_bricks.add(current_top_brick[x][y])
                    else:
                        pass
            # store support
            self.bricks[i].supported_by = top_bricks
            # update location
            self.bricks[i].z_high = top_z + 1 + \
                self.bricks[i].z_high - self.bricks[i].z_low
            if self.bricks[i].z_low != top_z + 1:
                number_of_bricks_moved += 1
                self.bricks[i].z_low = top_z + 1
            # update current top
            for x in range(self.bricks[i].x_low, self.bricks[i].x_high + 1):
                for y in range(self.bricks[i].y_low, self.bricks[i].y_high + 1):
                    current_top_z[x][y] = self.bricks[i].z_high
                    current_top_brick[x][y] = self.bricks[i].line_index
        return number_of_bricks_moved

    def compute_removable_bricks(self):
        removable_bricks = {brick.line_index for brick in self.bricks}
        for brick in self.bricks:
            if len(brick.supported_by) == 1:
                removable_bricks.discard(list(brick.supported_by)[0])
        return removable_bricks

    def remove_brick(self, brick_index):
        self.bricks.pop(brick_index)


class Brick():
    def __init__(self, line, line_index):
        self.line = line
        self.line_index = line_index
        self.re_line = [int(num) for num in re.findall('[0-9]+', line)]
        self.x_low = self.re_line[0]
        self.y_low = self.re_line[1]
        self.z_low = self.re_line[2]
        self.x_high = self.re_line[3]
        self.y_high = self.re_line[4]
        self.z_high = self.re_line[5]
        assert self.x_low <= self.x_high
        assert self.y_low <= self.y_high
        assert self.z_low <= self.z_high


ans = 0
for i in tqdm(range(len(lines))):
    stack = SandStack(lines)
    stack.drop_all_bricks()
    stack.remove_brick(i)
    ans += stack.drop_all_bricks()
print('ans', ans)
