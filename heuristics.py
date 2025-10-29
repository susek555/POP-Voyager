import networkx as nx
from path import Path
import random


def full_random(graph: nx.Graph, max_nodes: int) -> Path:
    path = Path(['P'])
    nodes = list(graph.nodes())
    nodes.remove('P')
    for i in range(0, max_nodes - 1):
        chosen_node = random.choice(nodes)
        path += chosen_node
        nodes.remove(chosen_node)
    return path + 'P'
