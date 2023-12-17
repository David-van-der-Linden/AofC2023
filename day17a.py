from my_secrets import path
import numpy as np

# code for creating graphs and applying Dijkstra's algorithm to it is taken from
# https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
# note it needed some modification in order to run

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = np.inf
        # Mark all nodes unvisited        
        self.visited = False
        # Predecessor
        self.previous = None
    
    def __lt__(self, other):
        return self.distance < other.distance

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start, target):
    print('''Dijkstra's shortest path''')
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                # print('updated : current = %s next = %s new_dist = %s' \
                #         %(current.get_id(), next.get_id(), next.get_distance()))
            else:
                # print('not updated : current = %s next = %s new_dist = %s' \
                #         %(current.get_id(), next.get_id(), next.get_distance()))
                pass

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

directions = {'R', 'L', 'U', 'D'}

dir_to_cords = {'R' : (0, 1),
                'L' : (0, -1),
                'U' : (-1, 0),
                'D' : (1, 0)}

dir_to_different_dir = {'R' : {'U', 'D'},
                        'L' : {'U', 'D'},
                        'U' : {'R', 'L'},
                        'D' : {'R', 'L'}}


if __name__ == '__main__':
    g = Graph()

    with open(path + 'test17.txt') as f:
        lines = f.read().split('\n')

    def ij_in_range(i,j):
        if 0 <= i < len(lines):
            if 0 <= j < len(lines[0]):
                return True
        return False

    max_straight = 3

    # add vertices
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            for d in directions:
                for straightness in range(1,max_straight+1):
                    g.add_vertex(f'{i},{j},{d}{straightness}')

    # add edges
    for old_i in range(len(lines)):
        for old_j in range(len(lines[0])):
            for old_d in directions:
                # changing directions
                for new_d in dir_to_different_dir[old_d]:
                    for straightness in range(1,max_straight+1):
                        new_i = old_i+dir_to_cords[new_d][0]
                        new_j = old_j+dir_to_cords[new_d][1]
                        if ij_in_range(new_i, new_j):
                            g.add_edge(f'{old_i},{old_j},{old_d}{straightness}',\
                                    f'{new_i},{new_j},{new_d}{1}', int(lines[new_i][new_j]))
                # keeping directions
                new_d = old_d
                new_i = old_i+dir_to_cords[new_d][0]
                new_j = old_j+dir_to_cords[new_d][1]
                if ij_in_range(new_i, new_j):
                    for straightness in range(1,max_straight):
                        g.add_edge(f'{old_i},{old_j},{old_d}{straightness}',\
                                f'{new_i},{new_j},{new_d}{straightness+1}', int(lines[new_i][new_j]))

    # since there are multiple end states lets add a end vertex
    # and costless edges to reach it from the other end states
    g.add_vertex('end')
    i = len(lines)-1
    j = len(lines[0])-1
    for d in ['D','R']:
        for straightness in range(1,max_straight+1):
            g.add_edge(f'{i},{j},{new_d}{straightness}', 'end', 0)
    
    # we also need to add a starting node with straightness zero
    g.add_vertex('start')
    g.add_edge('start', f'{0},{1},R{1}', int(lines[0][1]))
    g.add_edge('start', f'{1},{0},D{1}', int(lines[1][0]))

    # print('Graph data:')
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

    dijkstra(g, g.get_vertex('start'), g.get_vertex('end')) 

    target = g.get_vertex('end')
    path = [target.get_id()]

    shortest(target, path)
    print('The shortest path : %s' %(path[::-1]))
    print('ans', target.distance)