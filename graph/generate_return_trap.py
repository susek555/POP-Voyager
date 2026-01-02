import math
import random

import networkx as nx

from graph.generate import calc_cost


def generate_trap_graph(
    n_nodes_line: int,
    n_nodes_circle: int,
    line_dist: float = 10.0,
    circle_radius: float = 15.0,
    reward_range: tuple[int, int] = (10, 20),
    cost_factor: float = 0.2,
    circle_multiplier: float = 2.0,
) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(0, 0, 0))

    idx = 1

    current_pos = [0, 0, 0]
    for _ in range(n_nodes_line):
        current_pos[0] += line_dist
        pos = (
            current_pos[0],
            current_pos[1] + random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
        G.add_node(f"s{idx}", reward=random.randint(*reward_range), pos=pos)
        idx += 1

    angle_step = 2 * math.pi / n_nodes_circle
    for i in range(n_nodes_circle):
        angle = i * angle_step
        pos = (
            circle_radius * math.cos(angle),
            circle_radius * math.sin(angle),
            random.uniform(-1, 1)
        )
        G.add_node(f"s{idx}", reward=random.randint(*reward_range)*circle_multiplier, pos=pos)
        idx += 1

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u['pos'], data_v['pos'], cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
