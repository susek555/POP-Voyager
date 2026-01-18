import random
from typing import Any

from models.graph import EdgesData, NodesData
from models.path import Path


# edges_data = list(nx.Graph.edges(data=True))
def get_costs_from_node(edges_data: EdgesData, path: Path) -> dict[str, Any]:
    current_node = path[-1]
    return {
        (dst if src == current_node else src): data["cost"]
        for src, dst, data in edges_data
        if src == current_node or dst == current_node
    }


# nodes_data = list(nx.Graph.nodes(data=True))
def get_rewards(nodes_data: NodesData, path: Path) -> dict[str, Any]:
    rewards = {node: data["reward"] for node, data in nodes_data if node != path[-1]}
    rewards.update({node: 0 for node in rewards if node in path})
    return rewards


# nodes_data = list(nx.Graph.nodes(data=True))
def get_random_path(nodes_data: NodesData, number_of_nodes: int, rng: random.Random) -> Path:
    nodes = []
    for _ in range(number_of_nodes):
        node = rng.choice([n for n in nodes_data[1:] if not nodes or n != nodes[-1]])
        nodes.append(node)
    return Path(["P"] + [node for node, data in nodes] + ["P"])


def get_random_path_no_duplicates(
    nodes_data: NodesData, number_of_nodes: int, rng: random.Random
) -> Path:
    available_nodes = [n for n, _ in nodes_data[1:]]
    chosen_nodes = rng.sample(available_nodes, k=min(number_of_nodes, len(available_nodes)))
    rng.shuffle(chosen_nodes)
    return Path(["P"] + chosen_nodes + ["P"])
