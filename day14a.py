from my_secrets import path

with open(path + 'input14.txt') as f:
    lines = f.read().split('\n')


class dish_obj():
    def __init__(self, lines):
        self.dish = [list(row) for row in lines]

    def move_O_up(self, i, j):
        assert self.dish[i][j] == 'O'
        self.dish[i][j] = '.'
        ni = i - 1
        while ni >= 0 and self.dish[ni][j] == '.':
            ni -= 1
        self.dish[ni + 1][j] = 'O'


obj = dish_obj(lines)
for i in range(len(obj.dish)):
    for j in range(len(obj.dish[0])):
        if obj.dish[i][j] == 'O':
            obj.move_O_up(i, j)

ans = 0
for row_index, row in enumerate(obj.dish):
    row_weight = len(obj.dish) - row_index
    for char in row:
        if char == 'O':
            ans += row_weight
print('ans', ans)
