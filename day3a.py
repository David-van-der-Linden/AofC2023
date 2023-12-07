import re
from my_secrets import path

with open(path + 'input3.txt') as f:
    lines = f.read().split('\n')

nums_np = ['1','2','3','4','5','6','7','8','9','0','.']
ans = 0

for line_index in range(len(lines)):
    line = lines[line_index]
    # print(line)
    matches = re.finditer('[0-9]+', line)
    for match in matches:
        match_done = False
        # print(match.group(), "start index", match.start(), "End index", match.end())
        # print('lines[line_index][match.start()-1]:', lines[line_index][match.start()-1])

        # horizontal starts at 0 or match.start()-1
        # ends at match.end()+1 or len(line)-1
        # vertical
        if match_done == False:

            x_start = max(0,match.start()-1)
            x_end = min(match.end(),len(line)-1)
            # print('x_start', x_start)
            # print('x_end', x_end)

            for j in range(x_start, x_end+1):
                if match_done == False:

                    y_start = max(0,line_index-1)
                    y_end = min(line_index+1,len(lines)-1)
                    # print('y_start:', y_start)
                    # print('y_end:', y_end)

                    for i in range(y_start,y_end+1):

                        # print(lines[i][j])

                        if not lines[i][j] in nums_np:

                            # print('notin!!!')
                            ans += int(match.group())
                            # print('added:' + match.group())
                            match_done = True
                            break

    # print(matches)
print(ans)