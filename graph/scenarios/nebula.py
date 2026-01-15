import math
import random
from dataclasses import dataclass

import networkx as nx

from graph.generate import calc_cost
from graph.params import GraphParams


@dataclass
class NebulaGraphParams(GraphParams):
    n_nodes: int = 40
    cloud_radius: float = 50.0
    nebula_center: tuple[float, float, float] = (20.0, 0.0, 0.0)
    nebula_radius: float = 15.0
    nebula_multiplier: float = 5.0
    reward_range: tuple[int, int] = (10, 30)
    cost_factor: float = 0.2


def generate_nebula_graph(params: NebulaGraphParams) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(0.0, 0.0, 0.0))

    for i in range(1, params.n_nodes + 1):
        phi = random.uniform(0, 2 * math.pi)
        theta = random.uniform(0, math.pi)
        r = params.cloud_radius * (random.random() ** (1 / 3))

        pos = (
            r * math.sin(theta) * math.cos(phi),
            r * math.sin(theta) * math.sin(phi),
            r * math.cos(theta),
        )
        G.add_node(f"s{i}", reward=random.randint(*params.reward_range), pos=pos)

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]

            base_cost = calc_cost(data_u["pos"], data_v["pos"], params.cost_factor)

            midpoint = (
                (data_u["pos"][0] + data_v["pos"][0]) / 2,
                (data_u["pos"][1] + data_v["pos"][1]) / 2,
                (data_u["pos"][2] + data_v["pos"][2]) / 2,
            )

            dist_to_nebula = math.sqrt(
                (midpoint[0] - params.nebula_center[0]) ** 2
                + (midpoint[1] - params.nebula_center[1]) ** 2
                + (midpoint[2] - params.nebula_center[2]) ** 2
            )

            final_cost = base_cost
            if dist_to_nebula < params.nebula_radius:
                final_cost *= params.nebula_multiplier

            G.add_edge(u, v, cost=final_cost)

    return G
