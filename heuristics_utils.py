import networkx as nx
from path import Path
from typing import Dict, Any
import random
from dataclasses import dataclass


class SAparams:
    n_iter: int
    start_temp: float
    decrease_factor: float


# edges_data = list(graph.edges(data=True))
def get_costs_from_node(edges_data: list, path: Path) -> Dict[str, Any]:
    current_node = path[-1]
    return {
        (dst if src == current_node else src): data["cost"]
        for src, dst, data in edges_data
        if src == current_node or dst == current_node
    }


# nodes_data = list(graph.nodes(data=True))
def get_rewards(nodes_data: list, path: Path) -> Dict[str, Any]:
    rewards = {node: data["reward"] for node, data in nodes_data if node != path[-1]}
    rewards.update({node: 0 for node in rewards.keys() if node in path})
    return rewards


# nodes_data = list(graph.nodes(data=True))
def get_random_path(nodes_data: list, number_of_nodes: int) -> Path:
    nodes = []
    for _ in range(number_of_nodes):
        node = random.choice([n for n in nodes_data[1:] if not nodes or n != nodes[-1]])
        nodes.append(node)
    return Path(["P"] + [node for node, data in nodes] + ["P"])


import random
from copy import deepcopy

import random
from copy import deepcopy

def replace_one_node(nodes_data: list, path: list) -> list:
    new_path = deepcopy(path)
    node_to_replace = random.randint(1, len(new_path) - 2)  # avoid start and end 'P'
    old_node = new_path[node_to_replace]

    node_names = [node for node, _ in nodes_data[1:]]

    possible_nodes = [
        n for n in node_names
        if n != old_node
        and n != new_path[node_to_replace - 1]
        and n != new_path[node_to_replace + 1]
    ]

    if not possible_nodes:
        return new_path

    new_path[node_to_replace] = random.choice(possible_nodes)

    return new_path




