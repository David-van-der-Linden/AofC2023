from my_secrets import path
import networkx as nx
import matplotlib.pyplot as plt

with open(path + 'input21.txt') as f:
    lines = f.read().split('\n')

# idea make a graph for the problem
# a grid graph without the # nodes
# get the distance to the source node for all plots
# since max_steps is even
# if the distance is even and less than max_steps
# then it reachable in max_steps number of steps

max_steps = 64
assert max_steps % 2 == 0

global G
G = nx.Graph()

def create_grid_graph(lines):
    # all accept bottom and right side
    for i in range(len(lines) - 1):
        for j in range(len(lines[0]) - 1):
            G.add_edge(f'{i},{j}', f'{i + 1},{j}', weight=1)
            G.add_edge(f'{i},{j}', f'{i},{j +1}', weight=1)
    # bottom
    i = len(lines) - 1
    for j in range(len(lines[0]) - 1):
        G.add_edge(f'{i},{j}', f'{i},{j + 1}', weight=1)
    # right
    j = len(lines[0]) - 1
    for j in range(len(lines[0]) - 1):
        G.add_edge(f'{i},{j}', f'{i + 1},{j}', weight=1)
    
def remove_ht_nodes():
    # remove nodes i,j with lines[i][j] == '#'
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == '#':
                G.remove_node(f'{i},{j}')

def get_starting_node(lines):
    # find starting node
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == 'S':
                return i, j
    assert False

create_grid_graph(lines)
remove_ht_nodes()
si, sj = get_starting_node(lines)

# speed minor speed improvement only check squares on the checkerboard patten
all_dist = nx.shortest_path_length(G, source=f'{si},{sj}', target=None, weight="weight", method='dijkstra')
ans = 0
for node in all_dist:
    # i = int(node.split(',')[0])
    # j = int(node.split(',')[1])
    dist = all_dist[node]
    if dist % 2 == 0 and dist <= max_steps:
        ans += 1
print('ans', ans)
