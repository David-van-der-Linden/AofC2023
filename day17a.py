from my_secrets import path
import networkx as nx

# idea create a digraph with nodes as states where we store
# location i,j and direction d and straightness 1 2 or 3
# connect edges according to exercise with weights
# connect a start end end node to all the possible start and end states
# using edges of weight 1 for the first move and weight zero for the end states
# apply a shortest path algorithm


directions = {'R', 'L', 'U', 'D'}

dir_to_cords = {'R': (0, 1),
                'L': (0, -1),
                'U': (-1, 0),
                'D': (1, 0)}

dir_to_different_dir = {'R': {'U', 'D'},
                        'L': {'U', 'D'},
                        'U': {'R', 'L'},
                        'D': {'R', 'L'}}

if __name__ == '__main__':
    g = nx.DiGraph()

    with open(path + 'input17.txt') as f:
        lines = f.read().split('\n')

    def ij_in_range(i, j):
        if 0 <= i < len(lines):
            if 0 <= j < len(lines[0]):
                return True
        return False

    max_straight = 3

    # add edges
    for old_i in range(len(lines)):
        for old_j in range(len(lines[0])):
            for old_d in directions:
                # changing directions
                for new_d in dir_to_different_dir[old_d]:
                    for straightness in range(1, max_straight+1):
                        new_i = old_i+dir_to_cords[new_d][0]
                        new_j = old_j+dir_to_cords[new_d][1]
                        if ij_in_range(new_i, new_j):
                            g.add_edge(f'{old_i},{old_j},{old_d}{straightness}',
                                       f'{new_i},{new_j},{new_d}{1}',
                                       weight=int(lines[new_i][new_j]))
                # keeping directions
                new_d = old_d
                new_i = old_i+dir_to_cords[new_d][0]
                new_j = old_j+dir_to_cords[new_d][1]
                if ij_in_range(new_i, new_j):
                    for straightness in range(1, max_straight):
                        g.add_edge(f'{old_i},{old_j},{old_d}{straightness}',
                                   f'{new_i},{new_j},{new_d}{straightness+1}',
                                   weight=int(lines[new_i][new_j]))

    # since there are multiple end states lets add a end vertex
    # and costless edges to reach it from the other end states
    i = len(lines)-1
    j = len(lines[0])-1
    for d in ['D', 'R']:
        for straightness in range(1, max_straight+1):
            g.add_edge(f'{i},{j},{d}{straightness}', 'end', weight=0)

    # we also need to add a starting node with straightness zero
    g.add_edge('start', f'{0},{1},R{1}', weight=int(lines[0][1]))
    g.add_edge('start', f'{1},{0},D{1}', weight=int(lines[1][0]))

    shortest_path = nx.shortest_path(
        g, source='start', target='end', weight='weight')
    shortest_path_length = nx.path_weight(g, shortest_path, weight="weight")
    print(shortest_path)
    print('ans', shortest_path_length)
