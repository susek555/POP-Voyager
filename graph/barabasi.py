import math
import random
from dataclasses import dataclass

import networkx as nx


@dataclass
class BarabasiRadialParams:
    n_nodes: int = 30
    step_distance: float = 10.0
    reward_range: tuple[int, int] = (10, 50)
    cost_factor: float = 0.2
    seed: int = 42


def generate_barabasi_radial_graph(params: BarabasiRadialParams) -> nx.Graph:
    rng = random.Random(params.seed)
    G = nx.Graph()

    G.add_node("P", reward=0, pos=(0.0, 0.0, 0.0))
    nodes_list = ["P"]

    for i in range(1, params.n_nodes + 1):
        node_id = f"s{i}"

        weights = [1.0 / (idx + 1) for idx, _ in enumerate(nodes_list)]
        parent_id = rng.choices(nodes_list, weights=weights, k=1)[0]
        parent_pos = G.nodes[parent_id]["pos"]

        phi = rng.uniform(0, 2 * math.pi)
        theta = rng.uniform(0, math.pi)

        dx = params.step_distance * math.sin(theta) * math.cos(phi)
        dy = params.step_distance * math.sin(theta) * math.sin(phi)
        dz = params.step_distance * math.cos(theta)

        pos = (parent_pos[0] + dx, parent_pos[1] + dy, parent_pos[2] + dz)

        G.add_node(node_id, reward=rng.randint(*params.reward_range), pos=pos)
        nodes_list.append(node_id)

    all_nodes = list(G.nodes(data=True))
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            u, data_u = all_nodes[i]
            v, data_v = all_nodes[j]

            dist = (
                sum((a - b) ** 2 for a, b in zip(data_u["pos"], data_v["pos"], strict=False)) ** 0.5
            )
            G.add_edge(u, v, cost=dist * params.cost_factor)

    return G
