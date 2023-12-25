from my_secrets import path
import networkx as nx

global lines
with open(path + 'input23.txt') as f:
    lines = f.read().split('\n')

global g
g = nx.DiGraph()

# idea create a following the rules of the exercise
# find the longest path from start to end
# by iterating over all simple paths from start to end
# and chose the longest


def add_e_to_nps(i, j):
    # add edges to neighboring periods
    if lines[i+1][j] == '.':
        g.add_edge(f'{i},{j}', f'{i+1},{j}', weight=1)
    if lines[i-1][j] == '.':
        g.add_edge(f'{i},{j}', f'{i-1},{j}', weight=1)
    if lines[i][j+1] == '.':
        g.add_edge(f'{i},{j}', f'{i},{j+1}', weight=1)
    if lines[i][j-1] == '.':
        g.add_edge(f'{i},{j}', f'{i},{j-1}', weight=1)


for i in range(1, len(lines)-1):
    for j in range(1, len(lines[0])-1):
        if lines[i][j] == '.':
            add_e_to_nps(i, j)
        elif lines[i][j] == '>':
            g.add_edge(f'{i},{j-1}', f'{i},{j}', weight=1)
            g.add_edge(f'{i},{j}', f'{i},{j+1}', weight=1)
        elif lines[i][j] == '<':
            g.add_edge(f'{i},{j+1}', f'{i},{j}', weight=1)
            g.add_edge(f'{i},{j}', f'{i},{j-1}', weight=1)
        elif lines[i][j] == 'v':
            g.add_edge(f'{i-1},{j}', f'{i},{j}', weight=1)
            g.add_edge(f'{i},{j}', f'{i+1},{j}', weight=1)
        elif lines[i][j] == '^':
            g.add_edge(f'{i+1},{j}', f'{i},{j}', weight=1)
            g.add_edge(f'{i},{j}', f'{i-1},{j}', weight=1)

g.add_edge('0,1', '1,1', weight=1)


def longest_simple_path(graph, source, target) -> int:
    longest_path_length = 0
    for path in nx.all_simple_paths(graph, source=source, target=target):
        if len(path) > longest_path_length:
            longest_path_length = len(path)
    return longest_path_length


ans = longest_simple_path(g, '0,1', f'{len(lines)-1},{len(lines[0])-2}') - 1
print(ans)
