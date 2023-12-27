from my_secrets import path
import re

with open(path + 'input22.txt') as f:
    lines = f.read().split('\n')

# idea sort all the bricks by there lowest z value
# then iterate over all the bricks starting with the lowest z value
# drop them down until they hit another brick
# do this by keeping track of the highest dropped point so far for every xy
# and then placing it on top of that instantly


class SandStack():
    def __init__(self, lines):
        self.lines = lines
        self.bricks = list()
        for brick_index, line in enumerate(lines):
            self.bricks.append(Brick(line, brick_index))

        max_x = max(self.bricks, key=lambda x: x.x_high).x_high
        max_y = max(self.bricks, key=lambda x: x.y_high).y_high
        self.current_top_z = [
            [0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        self.current_top_brick = [
            ['the ground' for _ in range(max_y + 1)] for _ in range(max_x + 1)]

    def drop_all_bricks(self):
        self.bricks.sort(key=lambda x: x.z_low)
        for brick in self.bricks:
            top_z = 0
            top_bricks = set()
            for x in range(brick.x_low, brick.x_high + 1):
                for y in range(brick.y_low, brick.y_high + 1):
                    if top_z < self.current_top_z[x][y]:
                        top_z = self.current_top_z[x][y]
                        top_bricks.clear()
                        top_bricks.add(self.current_top_brick[x][y])
                    elif top_z == self.current_top_z[x][y]:
                        top_bricks.add(self.current_top_brick[x][y])
                    else:
                        pass
            # store support
            brick.supported_by = top_bricks
            # update location
            brick.z_high = top_z + 1 + brick.z_high - brick.z_low
            brick.z_low = top_z + 1
            # update current top
            for x in range(brick.x_low, brick.x_high + 1):
                for y in range(brick.y_low, brick.y_high + 1):
                    self.current_top_z[x][y] = brick.z_high
                    self.current_top_brick[x][y] = brick.brick_index

    def compute_removable_bricks(self):
        removable_bricks = {brick.brick_index for brick in self.bricks}
        for brick in self.bricks:
            if len(brick.supported_by) == 1:
                removable_bricks.discard(list(brick.supported_by)[0])
        return removable_bricks


class Brick():
    def __init__(self, line, brick_index):
        self.line = line
        self.brick_index = brick_index
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


stack = SandStack(lines)
stack.drop_all_bricks()
print('ans', len(stack.compute_removable_bricks()))
