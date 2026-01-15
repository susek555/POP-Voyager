import math
import random
from dataclasses import dataclass

import networkx as nx

from graph.generate import calc_cost
from graph.params import GraphParams


@dataclass
class SirenSongGraphParams(GraphParams):
    n_local_nodes: int = 20
    local_dist_range: tuple[float, float] = (5.0, 15.0)
    local_reward_range: tuple[int, int] = (5, 10)
    siren_distance: float = 100.0
    siren_reward: int = 500
    cost_factor: float = 0.2


def generate_siren_song_graph(params: SirenSongGraphParams) -> nx.Graph:
    G = nx.Graph()
    G.add_node("P", reward=0, pos=(0.0, 0.0, 0.0))

    idx = 1
    for _ in range(params.n_local_nodes):
        phi = random.uniform(0, 2 * math.pi)
        theta = random.uniform(0, math.pi)
        r = random.uniform(*params.local_dist_range)

        pos = (
            r * math.sin(theta) * math.cos(phi),
            r * math.sin(theta) * math.sin(phi),
            r * math.cos(theta),
        )
        G.add_node(f"s{idx}", reward=random.randint(*params.local_reward_range), pos=pos)
        idx += 1

    siren_pos = (params.siren_distance, 0.0, 0.0)
    G.add_node("SIREN", reward=params.siren_reward, pos=siren_pos)

    nodes = list(G.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, data_u = nodes[i]
            v, data_v = nodes[j]
            cost = calc_cost(data_u["pos"], data_v["pos"], params.cost_factor)
            G.add_edge(u, v, cost=cost)

    return G
