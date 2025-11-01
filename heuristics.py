import networkx as nx
from path import Path
import random


def full_random(graph: nx.Graph, max_nodes: int) -> Path:
    path = Path(["P"])
    nodes = list(graph.nodes())
    nodes.remove("P")
    for i in range(0, max_nodes):
        chosen_node = random.choice(nodes)
        path += chosen_node
        nodes.remove(chosen_node)
    return path + "P"


def greedy(graph: nx.Graph, max_nodes: int) -> Path:
    path = Path(["P"])
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    current_node = "P"
    visited = []

    for i in range(0, max_nodes):
        costs = {
            (dst if src == current_node else src): data["cost"]
            for src, dst, data in edges_data
            if src == current_node or dst == current_node
        }
        rewards = {
            node: data["reward"] for node, data in nodes_data if node != current_node
        }
        rewards.update({node: 0 for node in rewards.keys() if node in visited})

        ratios = {
            node: rewards[node] / costs[node] for node in rewards if node in costs
        }

        next_node = max(ratios, key=ratios.get)
        path += next_node
        visited.append(next_node)
        current_node = next_node

    return path + "P"
