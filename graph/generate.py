import random
from dataclasses import dataclass

import networkx as nx

from graph.params import GraphParams


@dataclass
class BasicGraphParams(GraphParams):
    number_of_nodes: int
    max_base_distance: float = 10.0
    reward_range: tuple[int, int] = (5, 20)
    cost_factor: float = 1.0


def generate_graph(
    params: BasicGraphParams,
) -> nx.Graph:
    graph = nx.Graph()
    graph.add_node("P", reward=0, pos=(0, 0, 0))

    for i in range(1, params.number_of_nodes):
        node_name = f"s{i}"
        reward = random.randint(*params.reward_range)
        pos = (
            random.uniform(-params.max_base_distance, params.max_base_distance),
            random.uniform(-params.max_base_distance, params.max_base_distance),
            random.uniform(-params.max_base_distance, params.max_base_distance),
        )
        graph.add_node(node_name, reward=reward, pos=pos)

    nodes = graph.nodes(data=True)

    for i, (node1, data1) in enumerate(nodes):
        for j, (node2, data2) in enumerate(nodes):
            if i < j:
                cost = calc_cost(data1["pos"], data2["pos"], params.cost_factor)
                graph.add_edge(node1, node2, cost=cost)

    return graph


# To avoid division by 0 if nodes have the exact same position
BIAS = 1


def calc_cost(
    pos1: tuple[float, float, float], pos2: tuple[float, float, float], factor: float
) -> int:
    return int(
        ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5
        * factor
        + BIAS
    )
