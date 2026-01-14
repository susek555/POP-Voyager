import random

import networkx as nx

from graph.generate import calc_cost


def generate_bottleneck_graph(
    nodes_per_side: int = 15,
    bridge_nodes: int = 1,
    side_distance: float = 40.0,
    bubble_radius: float = 10.0,
    reward_range: tuple[int, int] = (10, 30),
    far_reward_multiplier: float = 2.5,
    cost_factor: float = 0.2
) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(-side_distance, 0.0, 0.0))

    idx = 1
    for _ in range(nodes_per_side):
        pos = (
            -side_distance + random.uniform(-bubble_radius, bubble_radius),
            random.uniform(-bubble_radius, bubble_radius),
            random.uniform(-bubble_radius, bubble_radius)
        )
        G.add_node(f"s{idx}", reward=random.randint(*reward_range), pos=pos)
        idx += 1

    for i in range(bridge_nodes):
        pos = (0.0, (i - bridge_nodes/2) * 5.0, 0.0)
        G.add_node(f"bridge_{i}", reward=random.randint(*reward_range), pos=pos)

    for _ in range(nodes_per_side):
        pos = (
            side_distance + random.uniform(-bubble_radius, bubble_radius),
            random.uniform(-bubble_radius, bubble_radius),
            random.uniform(-bubble_radius, bubble_radius)
        )
        reward = int(random.randint(*reward_range) * far_reward_multiplier)
        G.add_node(f"s{idx}", reward=reward, pos=pos)
        idx += 1

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u["pos"], data_v["pos"], cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
