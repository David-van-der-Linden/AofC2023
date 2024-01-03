from my_secrets import path
import networkx as nx
from tqdm import tqdm

with open(path + 'input21.txt') as f:
    lines = f.read().split('\n')

# idea when looking at the input you can see that this problem is drastically
# easier due to the padding of . around the edges and in a cross shape around the S
# this makes it so that any shortest path can go in a straight line
# till its at the right x chuck cord
# then do a 90 turn and move until its at the correct y chunk cord
# and after that move locally

# todo use more functions

# note the max_steps is now odd so we have to adjust our code accordingly
max_steps = 26501365
assert max_steps % 2 == 1

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
    for i in range(len(lines) - 1):
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


# compute all distances starting from different positions
dist_t_l = nx.shortest_path_length(G, source=f'{0},{0}')
dist_t_m = nx.shortest_path_length(G, source=f'{0},{sj}')
dist_t_r = nx.shortest_path_length(G, source=f'{0},{len(lines[0])-1}')
dist_m_l = nx.shortest_path_length(G, source=f'{si},{0}')
dist_m_m = nx.shortest_path_length(G, source=f'{si},{sj}')
dist_m_r = nx.shortest_path_length(G, source=f'{si},{len(lines[0])-1}')
dist_b_l = nx.shortest_path_length(G, source=f'{len(lines)-1},{0}')
dist_b_m = nx.shortest_path_length(G, source=f'{len(lines)-1},{sj}')
dist_b_r = nx.shortest_path_length(
    G, source=f'{len(lines)-1},{len(lines[0])-1}')

# idea go over all 8 cardinal directions and the center to add there area
# plan in pseudo code
# for chunk in top left quadrant
# compute distance to starting garden plot (starting_dist)
# add 1 to ans all garden plots that satisfy
# (chunk_dist + starting_dist <= max_steps) and (chunk_dist + starting_dist) % 2 == 1
# we can speed this up by skipping the computation for all chunks that have a starting distance
# so low that all tiles that are reachable with any distance are within the max_steps

# lets compute the center nodes
ans = 0
for node in dist_m_m:
    # i = int(node.split(',')[0])
    # j = int(node.split(',')[1])
    dist = dist_m_m[node]
    if dist % 2 == 1 and dist <= max_steps:
        ans += 1


def compute_diagonal(max_steps, vertical_len_chunk, horizontal_len_chunk, leave_center_dist, max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd):
    assert vertical_len_chunk % 2 == 1
    assert horizontal_len_chunk % 2 == 1
    nr_of_plots = 0
    temp_dict = dict()
    for chunk_i in tqdm(range((max_steps // vertical_len_chunk) + 5)):
        # consider
        # starting_dist = max_steps - max_dist_in_chunk - 10
        # starting_dist = leave_center_dist + chunk_i * vertical_len_chunk + chunk_j * horizontal_len_chunk
        # rewriting yields
        # chunk_j * horizontal_len_chunk =  max_steps - max_dist_in_chunk - 10 - (leave_center_dist + chunk_i * vertical_len_chunk)
        # chunk_j = (max_steps - max_dist_in_chunk - 10 - (leave_center_dist + chunk_i * vertical_len_chunk)) // horizontal_len_chunk
        # if we ensure that our range starts at an even numbered chunk index
        # then an even number of chunks have been before it
        # so then the number of plots in those chunks before that are
        # (max_reachable_even + max_reachable_odd) * 1/2 number_of_skipped_chunks
        range_start = ((((max_steps - max_dist_in_chunk - 10 - (leave_center_dist +
                       chunk_i * vertical_len_chunk)) // horizontal_len_chunk) // 2) * 2) - 2
        number_of_skipped_chunks = range_start
        assert number_of_skipped_chunks % 2 == 0
        if number_of_skipped_chunks > 0:
            nr_of_plots += (max_reachable_even + max_reachable_odd) * \
                1/2 * number_of_skipped_chunks
        else:
            range_start = 0
        # similarly the we can find when the range should end by rewriting
        # starting_dist = max_steps
        # starting_dist = leave_center_dist + chunk_i * vertical_len_chunk + chunk_j * horizontal_len_chunk
        # chunk_j = ((starting_dist - leave_center_dist - chunk_i * vertical_len_chunk) // horizontal_len_chunk) + 1
        range_end = ((max_steps - leave_center_dist - chunk_i *
                     vertical_len_chunk) // horizontal_len_chunk) + 5
        for chunk_j in range(range_start, range_end):
            starting_dist = leave_center_dist + \
                chunk_i * vertical_len_chunk + \
                chunk_j * horizontal_len_chunk
            if starting_dist > max_steps + 5:
                break  # chunk is unreachable we add nothing
            elif starting_dist < max_steps - max_dist_in_chunk - 10:
                # chunk is ez to reach add the maximum
                # since the max_steps is odd we add the
                # evenly reachable number if starting dist is odd
                # and the odyl reachable number if the starting dist is even
                nr_of_plots += max_reachable_even if \
                    (starting_dist % 2 == 1) else max_reachable_odd
            elif starting_dist in temp_dict:
                nr_of_plots += temp_dict[starting_dist]
            else:
                # some of the garden plots might be reachable while others are not
                # lets simulate it
                counter = 0
                for node in relevant_chunk:
                    dist = relevant_chunk[node] + starting_dist
                    if dist <= max_steps and dist % 2 == 1:
                        counter += 1
                temp_dict[starting_dist] = counter
                nr_of_plots += counter
    return nr_of_plots


# chunks in top left direction from center
# lets say that the coordinates are as follows
# 1,1 1,0 n n
# 0,1 0,0 n n
#  n   n  s n
#  n   n  n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_b_r
leave_center_dist = dist_m_m['0,0'] + 2
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
vertical_len_chunk = len(lines)

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_diagonal(max_steps, vertical_len_chunk, horizontal_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)

# chunks in top right direction from center
# lets say that the coordinates are as follows
#  n   n  n 1,0 1,1
#  n   n  n 0,0 0,1
#  n   n  s  n   n
#  n   n  n  n   n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_b_l
leave_center_dist = dist_m_m[f'0,{len(lines[0])-1}'] + 2
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
vertical_len_chunk = len(lines)

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_diagonal(max_steps, vertical_len_chunk, horizontal_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)

# chunks in bottom right direction from center
# lets say that the coordinates are as follows
#  n   n  n  n   n
#  n   n  s  n   n
#  n   n  n 0,0 0,1
#  n   n  n 1,0 1,1
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_t_l
leave_center_dist = dist_m_m[f'{len(lines)-1},{len(lines[0])-1}'] + 2
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
vertical_len_chunk = len(lines)

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_diagonal(max_steps, vertical_len_chunk, horizontal_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)


# chunks in bottom left direction from center
# lets say that the coordinates are as follows
#  n   n  n n
#  n   n  s n
# 0,1 0,0 n n
# 1,1 1,0 n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_t_r
leave_center_dist = dist_m_m[f'{len(lines)-1},0'] + 2
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
vertical_len_chunk = len(lines)

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_diagonal(max_steps, vertical_len_chunk, horizontal_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)


def compute_straight(max_steps, relevant_len_chunk, leave_center_dist, max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd):
    assert relevant_len_chunk % 2 == 1
    nr_of_plots = 0
    # todo start range close to max_steps // relevant_len_chunk
    for chunk_i in tqdm(range((max_steps // relevant_len_chunk) + 5)):
        starting_dist = leave_center_dist + \
            chunk_i * relevant_len_chunk
        if starting_dist > max_steps + 5:
            break  # chunk is unreachable we add nothing
        elif starting_dist < max_steps - max_dist_in_chunk - 10:
            # chunk is ez to reach add the maximum
            # since the max_steps is odd we add the
            # evenly reachable number if starting dist is odd
            # and the odyl reachable number if the starting dist is even
            nr_of_plots += max_reachable_even if \
                (starting_dist % 2 == 1) else max_reachable_odd
        else:
            # some of the garden plots might be reachable while others are not
            # lets simulate it
            counter = 0
            for node in relevant_chunk:
                dist = relevant_chunk[node] + starting_dist
                if dist <= max_steps and dist % 2 == 1:
                    counter += 1
            nr_of_plots += counter
    return nr_of_plots


# chunks in left direction from center
# lets say that the coordinates are as follows
#  n n n n
#  1 0 s n
#  n n n n
#  n n n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_m_r
leave_center_dist = dist_m_m[f'{si},{len(lines[0])-1}'] + 1
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
relevant_len_chunk = horizontal_len_chunk

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_straight(max_steps, relevant_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)

# chunks in right direction from center
# lets say that the coordinates are as follows
#  n n n n n
#  n n s 0 1
#  n n n n n
#  n n n n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_m_l
leave_center_dist = dist_m_m[f'{si},{0}'] + 1
max_dist_in_chunk = max(relevant_chunk.values())

horizontal_len_chunk = len(lines[0])
relevant_len_chunk = horizontal_len_chunk

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_straight(max_steps, relevant_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)

# chunks in down direction from center
# lets say that the coordinates are as follows
#  n n n n n
#  n n s n n
#  n n 0 n n
#  n n 1 n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_t_m
leave_center_dist = dist_m_m[f'{len(lines)-1},{sj}'] + 1
max_dist_in_chunk = max(relevant_chunk.values())

vertical_len_chunk = len(lines)
relevant_len_chunk = vertical_len_chunk

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_straight(max_steps, relevant_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)

# chunks in upward direction from center
# lets say that the coordinates are as follows
#  n n 1 n n
#  n n 0 n n
#  n n s n n
#  n n n n n
# here s denotes the center and n are chunks that are not relevant
relevant_chunk = dist_b_m
leave_center_dist = dist_m_m[f'{0},{sj}'] + 1
max_dist_in_chunk = max(relevant_chunk.values())

vertical_len_chunk = len(lines)
relevant_len_chunk = vertical_len_chunk

max_reachable_even = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 0) and
     (relevant_chunk[node] <= max_steps)])
max_reachable_odd = len(
    [1 for node in relevant_chunk if (relevant_chunk[node] % 2 == 1) and
     (relevant_chunk[node] <= max_steps)])

ans += compute_straight(max_steps, relevant_len_chunk, leave_center_dist,
                        max_dist_in_chunk, relevant_chunk, max_reachable_even, max_reachable_odd)
print('ans', int(ans))
