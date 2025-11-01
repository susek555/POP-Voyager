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
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    path = Path(["P"])

    for i in range(0, max_nodes):
        costs = heuristics_utils.get_costs_from_node(edges_data, path)
        rewards = heuristics_utils.get_rewards(nodes_data, path)

        ratios = {
            node: rewards[node] / costs[node] for node in rewards if node in costs
        }

        next_node = max(ratios, key=ratios.get)
        path += next_node

    return path + "P"


def SA(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: heuristics_utils.SAparams,
) -> Path:
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    best_path = heuristics_utils.get_random_path(nodes_data, max_nodes)
    best_eval = objective_function(graph, best_path)
    current_path, current_eval = best_path, best_eval
    scores = [best_eval]

    print(best_path)
    print(heuristics_utils.replace_one_node(nodes_data, best_path))

    # for i in range(params.n_iter):

    raise (Exception)
