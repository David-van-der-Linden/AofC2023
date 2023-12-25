from my_secrets import path
import networkx as nx
from tqdm import tqdm

global lines
with open(path + 'input23.txt') as f:
    lines = f.read().split('\n')

global g
g = nx.Graph()

# idea make an undirected graph and remove all vertices with degree 2
# and replace them by an edge with the sum of the weighted edges it had before


def add_e_to_nnhs_br(i, j):
    # add edges to neighboring non hashtags to bottom and right only
    if lines[i+1][j] != '#':
        g.add_edge(f'{i},{j}', f'{i+1},{j}', weight=1)
    if lines[i][j+1] != '#':
        g.add_edge(f'{i},{j}', f'{i},{j+1}', weight=1)


for i in range(1, len(lines)-1):
    for j in range(1, len(lines[0])-1):
        if lines[i][j] != '#':
            add_e_to_nnhs_br(i, j)

g.add_edge('0,1', '1,1', weight=1)


def replace_vertex_w_edge(vertex):
    assert g.degree(vertex) == 2
    lst = list(g.neighbors(vertex))
    w0 = g[lst[0]][vertex]['weight']
    w1 = g[lst[1]][vertex]['weight']
    g.remove_node(vertex)
    g.add_edge(lst[0], lst[1], weight=w0+w1)


def condense_graph():
    deg_2_nodes = [n for n in g.nodes if g.degree(n) == 2]
    while len(deg_2_nodes) > 0:
        replace_vertex_w_edge(deg_2_nodes[0])
        deg_2_nodes.pop(0)
    assert len([n for n in g.nodes if g.degree(n) == 2]) == 0


def longest_simple_path(graph, source, target) -> int:
    longest_path_length = 0
    for path in tqdm(nx.all_simple_paths(graph, source=source, target=target)):
        if nx.path_weight(g, path, weight='weight') > longest_path_length:
            longest_path_length = nx.path_weight(g, path, weight='weight')
    return longest_path_length


print('number of nodes before condensing', len(g.nodes))
condense_graph()
print('number of nodes after condensing', len(g.nodes))
ans = longest_simple_path(g, '0,1', f'{len(lines)-1},{len(lines[0])-2}')
print('ans', ans)
