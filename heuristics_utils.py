import networkx as nx
from path import Path
from typing import Dict, Any


# edges_data = list(graph.edges(data=True))
def get_costs_from_node(
    edges_data: list[tuple[Any, Any, dict[str, Any]]], path: Path
) -> Dict[str, Any]:
    current_node = path[-1]
    return {
        (dst if src == current_node else src): data["cost"]
        for src, dst, data in edges_data
        if src == current_node or dst == current_node
    }


# nodes_data = list(graph.nodes(data=True))
def get_rewards(nodes_data: list, path: Path):
    rewards = {node: data["reward"] for node, data in nodes_data if node != path[-1]}
    rewards.update({node: 0 for node in rewards.keys() if node in path})
    return rewards
