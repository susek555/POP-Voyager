import random

import networkx as nx

from models.path import Path


def full_random(graph: nx.Graph, max_nodes: int) -> Path:
    path = Path(["P"])
    nodes = list(graph.nodes())
    nodes.remove("P")
    for _i in range(0, max_nodes):
        chosen_node = random.choice(nodes)
        path += chosen_node
        nodes.remove(chosen_node)
    return path + "P"
