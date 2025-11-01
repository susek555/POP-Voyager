import networkx as nx
from path import Path
import random
from typing import Callable
import heuristics_utils


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

    for i in range(0, max_nodes):
        costs = heuristics_utils.get_costs_from_node(edges_data, path)
        rewards = heuristics_utils.get_rewards(nodes_data, path)

        ratios = {
            node: rewards[node] / costs[node] for node in rewards if node in costs
        }

        next_node = max(ratios, key=ratios.get)
        path += next_node

    return path + "P"

def SA(graph: nx.Graph, objective_function: Callable[[nx.Graph, Path], float], max_nodes: int) -> Path:


    raise(Exception)
