import networkx as nx

import utils
from models.graph import EdgesData, NodesData
from models.path import Path


def greedy(graph: nx.Graph, max_nodes: int) -> Path:
    nodes_data: NodesData = list(graph.nodes(data=True))
    edges_data: EdgesData = list(graph.edges(data=True))
    path = Path(["P"])

    for _i in range(0, max_nodes):
        costs = utils.get_costs_from_node(edges_data, path)
        rewards = utils.get_rewards(nodes_data, path)

        ratios = {node: rewards[node] / costs[node] for node in rewards if node in costs}

        next_node = max(ratios, key=ratios.get)
        path += next_node

    return path + "P"
