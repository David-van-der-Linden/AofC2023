import re
from my_secrets import path

with open(path + 'input3.txt') as f:
    lines = f.read().split('\n')

# keys are (i,j) pairs that map to a list of numbers
# (i,j) is the coordinates of a * the numbers are the adjacent numbers
my_dict = {}

for line_index in range(len(lines)):
    line = lines[line_index]
    matches = re.finditer('[0-9]+', line)
    for match in matches:
        match_done = False
        if not match_done:
            # horizontal box starts at x_start and ends at x_end
            x_start = max(0,match.start()-1)
            x_end = min(match.end(),len(line)-1)
            for j in range(x_start, x_end+1):
                if not match_done:
                    # vertical box starts at y_start and ends at y_end
                    y_start = max(0,line_index-1)
                    y_end = min(line_index+1,len(lines)-1)
                    for i in range(y_start,y_end+1):
                        if lines[i][j] in '*':
                            my_dict.setdefault((i,j),[]).append(match.group())
                            match_done = True
                            break

# get the sum of products
ans = 0
for key in my_dict:
    if len(my_dict[key]) == 2:
        ans += int(my_dict[key][0])*int(my_dict[key][1])
print(ans)