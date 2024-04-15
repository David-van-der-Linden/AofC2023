import re
from my_secrets import path

with open(path + 'input3.txt') as f:
    lines = f.read().split('\n')

nums_np = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
ans = 0

# idea create a box around all numbers and check for symbols in that box that are not numbers or periods
for line_index in range(len(lines)):
    line = lines[line_index]
    matches = re.finditer('[0-9]+', line)
    for match in matches:
        match_done = False
        if not match_done:
            # horizontal box starts at x_start and ends at x_end
            x_start = max(0, match.start()-1)
            x_end = min(match.end(), len(line)-1)
            for j in range(x_start, x_end+1):
                if not match_done:
                    # vertical box starts at y_start and ends at y_end
                    y_start = max(0, line_index-1)
                    y_end = min(line_index+1, len(lines)-1)
                    for i in range(y_start, y_end+1):
                        if lines[i][j] not in nums_np:
                            ans += int(match.group())
                            match_done = True
                            break

print(ans)
