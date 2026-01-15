import math
import random
from dataclasses import dataclass

import networkx as nx

from graph.generate import calc_cost
from graph.params import GraphParams


@dataclass
class GradientGraphParams(GraphParams):
    n_nodes: int = 50
    max_dist: float = 100.0
    base_reward: int = 10
    reward_scaling: float = 2.0
    cost_factor: float = 0.2


def generate_gradient_graph(params: GradientGraphParams) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(0.0, 0.0, 0.0))

    for i in range(1, params.n_nodes + 1):
        phi = random.uniform(0, 2 * math.pi)
        theta = random.uniform(0, math.pi)
        r = random.uniform(10, params.max_dist)

        pos = (
            r * math.sin(theta) * math.cos(phi),
            r * math.sin(theta) * math.sin(phi),
            r * math.cos(theta),
        )

        reward = int(params.base_reward + (r * params.reward_scaling))

        G.add_node(f"s{i}", reward=reward, pos=pos)

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u["pos"], data_v["pos"], params.cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
