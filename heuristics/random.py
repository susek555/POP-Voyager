import random

import networkx as nx

from models.path import Path
from utils.config import AlgorithmParams


def full_random(graph: nx.Graph, max_nodes: int, params: AlgorithmParams) -> Path:
    rng = random.Random(params.seed)
    path = Path(["P"])
    nodes = list(graph.nodes())
    nodes.remove("P")
    for _i in range(0, max_nodes):
        chosen_node = rng.choice(nodes)
        path += chosen_node
        nodes.remove(chosen_node)
    return path + "P"
