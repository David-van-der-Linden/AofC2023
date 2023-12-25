from my_secrets import path
import networkx as nx

with open(path + 'input25.txt') as f:
    lines = f.read().split('\n')

# create graph
g = nx.Graph()
for line in lines:
    line = line.split(':')
    left_node = line[0]
    right_nodes = line[1].split()
    for right_node in right_nodes:
        g.add_edge(left_node, right_node, weight=1)

# get minimum cut
cut = nx.minimum_edge_cut(g)
assert len(cut) == 3
for edge in cut:
    g.remove_edge(edge[0], edge[1])

assert nx.number_connected_components(g) == 2
ans = 1
for component in nx.connected_components(g):
    ans = ans * len(component)
print('ans', ans)