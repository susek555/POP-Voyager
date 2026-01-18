from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

import networkx as nx

from models.graph import EdgesData, NodesData
from models.path import Path
from utils.config import AlgorithmParams


class ChildrenFactory(Enum):
    ALL = 1
    N_BEST = 2


@dataclass(kw_only=True)
class AStarParams(AlgorithmParams):
    childrenFactory: ChildrenFactory = ChildrenFactory.ALL
    n_children: int = 10


# nodes_data= list(nx.Graph.nodes(data=True))
def find_n_best_nodes(nodes_data: NodesData, n: int) -> list:
    node_rewards = {node: data["reward"] for node, data in nodes_data if node != "P"}
    sorted_nodes = sorted(
        node_rewards.items(), key=lambda item: item[1], reverse=True
    )  # best first
    best_nodes = list(sorted_nodes[:n])
    return best_nodes


# edges_data = list(nx.Graph.edges(data=True))
def find_n_best_edges(edges_data: EdgesData, n: int) -> list:
    edge_costs = {
        (src, dst): data["cost"] for src, dst, data in edges_data if src != "P" and dst != "P"
    }
    sorted_edges = sorted(edge_costs.items(), key=lambda item: item[1])  # best first
    best_edges = list(sorted_edges[:n])
    return best_edges


@lru_cache(maxsize=0)
def calc_best_theoretical_objective(
    graph: nx.Graph, best_nodes: NodesData, best_edges: EdgesData, path: Path
) -> float:
    edges_in_path = [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

    current_edges_set = set()
    for edge in edges_in_path:
        current_edges_set.add(edge)
        current_edges_set.add((edge[1], edge[0]))
    available_best_edges = []
    for edge, cost in best_edges:
        if edge not in current_edges_set and (edge[1], edge[0]) not in current_edges_set:
            available_best_edges.append((edge, cost))

    available_best_nodes = []
    for node, reward in best_nodes:
        if node not in path:
            available_best_nodes.append((node, reward))

    total_reward = sum(graph.nodes[node]["reward"] for node in set(path))
    nodes_to_add = len(best_nodes) - len(path) + 1
    for i in range(nodes_to_add):
        total_reward += available_best_nodes[i][1]
    total_cost = sum(graph[u][v]["cost"] for u, v in edges_in_path)
    edges_to_add = len(best_edges) - len(edges_in_path)
    for i in range(edges_to_add):
        total_cost += available_best_edges[i][1]

    return total_reward / total_cost


def get_children(nodes_data: NodesData, path: Path) -> list[Path]:
    return [path + node for node, _ in nodes_data[1:] if node != path[-1]]


def get_n_best_children(
    nodes_data: NodesData, edges_data: EdgesData, path: Path, n: int
) -> list[Path]:
    possible_neighbors = [node for node, _ in nodes_data[1:] if node != path]
    if len(possible_neighbors) <= n:
        return [path + node for node in possible_neighbors]
    edge_costs = {(src, dst): data["cost"] for src, dst, data in edges_data}
    neighbors_score = {
        node: edge_costs.get((path[-1], node), edge_costs.get((node, path[-1])))
        for node in possible_neighbors
        if (path[-1], node) in edge_costs or (node, path[-1]) in edge_costs
    }
    sorted_neighbors = sorted(neighbors_score.items(), key=lambda item: item[1])
    children = []
    for i in range(n):
        children.append(path + sorted_neighbors[i][0])
    return children
