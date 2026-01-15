import random
from dataclasses import dataclass

import networkx as nx

from graph.config import GraphParams
from graph.generate import calc_cost


@dataclass
class BottleneckGraphParams(GraphParams):
    nodes_per_side: int = 15
    bridge_nodes: int = 1
    side_distance: float = 40.0
    bubble_radius: float = 10.0
    reward_range: tuple[int, int] = (10, 30)
    far_reward_multiplier: float = 2.5
    cost_factor: float = 0.2


def generate_bottleneck_graph(params: BottleneckGraphParams) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(-params.side_distance, 0.0, 0.0))

    idx = 1
    for _ in range(params.nodes_per_side):
        pos = (
            -params.side_distance + random.uniform(-params.bubble_radius, params.bubble_radius),
            random.uniform(-params.bubble_radius, params.bubble_radius),
            random.uniform(-params.bubble_radius, params.bubble_radius),
        )
        G.add_node(f"s{idx}", reward=random.randint(*params.reward_range), pos=pos)
        idx += 1

    for i in range(params.bridge_nodes):
        pos = (0.0, (i - params.bridge_nodes / 2) * 5.0, 0.0)
        G.add_node(f"bridge_{i}", reward=random.randint(*params.reward_range), pos=pos)

    for _ in range(params.nodes_per_side):
        pos = (
            params.side_distance + random.uniform(-params.bubble_radius, params.bubble_radius),
            random.uniform(-params.bubble_radius, params.bubble_radius),
            random.uniform(-params.bubble_radius, params.bubble_radius),
        )
        reward = int(random.randint(*params.reward_range) * params.far_reward_multiplier)
        G.add_node(f"s{idx}", reward=reward, pos=pos)
        idx += 1

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u["pos"], data_v["pos"], params.cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
