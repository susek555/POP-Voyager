import random
from dataclasses import dataclass

import networkx as nx

from graph.generate import calc_cost
from graph.params import GraphParams


@dataclass
class ArchipelagoGraphParams(GraphParams):
    n_clusters: int = 3
    nodes_per_cluster: int = 10
    cluster_spread: float = 5.0
    map_size: float = 100.0
    reward_range: tuple[int, int] = (10, 50)
    cost_factor: float = 0.2


def generate_archipelago_graph(params: ArchipelagoGraphParams) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(0.0, 0.0, 0.0))

    idx = 1
    for _ in range(params.n_clusters):
        center = (
            random.uniform(-params.map_size, params.map_size),
            random.uniform(-params.map_size, params.map_size),
            random.uniform(-params.map_size, params.map_size),
        )

        for _ in range(params.nodes_per_cluster):
            pos = (
                center[0] + random.uniform(-params.cluster_spread, params.cluster_spread),
                center[1] + random.uniform(-params.cluster_spread, params.cluster_spread),
                center[2] + random.uniform(-params.cluster_spread, params.cluster_spread),
            )
            G.add_node(f"s{idx}", reward=random.randint(*params.reward_range), pos=pos)
            idx += 1

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u["pos"], data_v["pos"], params.cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
