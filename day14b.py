from my_secrets import path
from copy import deepcopy
from tqdm import tqdm

with open(path + 'test14.txt') as f:
	lines = f.read().split('\n')

print('pre')
for line in lines:
	print(line)
print('\npost')

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
	
	def move_O_down(self, i, j):
		assert self.dish[i][j] == 'O'
		self.dish[i][j] = '.'
		ni = i + 1
		while ni <= len(self.dish) - 1 and \
				  self.dish[ni][j] == '.':
			ni += 1
		self.dish[ni - 1][j] = 'O'
	
	def move_O_left(self, i, j):
		assert self.dish[i][j] == 'O'
		self.dish[i][j] = '.'
		nj = j - 1
		while nj >= 0 and self.dish[i][nj] == '.':
			nj -= 1
		self.dish[i][nj + 1] = 'O'
	
	def move_O_right(self, i, j):
		assert self.dish[i][j] == 'O'
		self.dish[i][j] = '.'
		nj = j + 1
		while nj <= len(self.dish[0]) -1 and \
				  self.dish[i][nj] == '.':
			nj += 1
		self.dish[i][nj - 1] = 'O'
		
	def move_all_up(self):
		for i in range(len(self.dish)):
			for j in range(len(self.dish[0])):
				if self.dish[i][j] == 'O':
					self.move_O_up(i, j)
		
	def move_all_down(self):
		for i in reversed(range(len(self.dish))):
			for j in range(len(self.dish[0])):
				if self.dish[i][j] == 'O':
					self.move_O_down(i, j)
		
	def move_all_right(self):
		for i in range(len(self.dish)):
			for j in reversed(range(len(self.dish[0]))):
				if self.dish[i][j] == 'O':
					self.move_O_right(i, j)
		
	def move_all_left(self):
		for i in range(len(self.dish)):
			for j in range(len(self.dish[0])):
				if self.dish[i][j] == 'O':
					self.move_O_left(i, j)
	
	def do_cycle(self):
		self.move_all_up()
		self.move_all_left()
		self.move_all_down()
		self.move_all_right()
	
	def visualize(self):
		for line in self.dish:
			print(''.join(line))

obj = dish_obj(lines)
for cycle_nr in tqdm(range(4)):#1000000000)):
	print('\ncycle_nr', cycle_nr)
	obj.visualize()
	last_dish = deepcopy(obj.dish)
	obj.do_cycle()
	if last_dish == obj.dish:
		break

ans = 0
for row_index, row in enumerate(obj.dish):
	row_weight = len(obj.dish) - row_index
	for char in row:
		if char == 'O':
			ans += row_weight
print('ans', ans)