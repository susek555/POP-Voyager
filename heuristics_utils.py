import networkx as nx
from path import Path
from typing import Dict, Any
import random
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class SAparams:
    n_iter: int
    start_temp: float
    decrease_factor: float
    n_threads: int
    n_candidates_per_thread: int


# edges_data = list(nx.Graph.edges(data=True))
def get_costs_from_node(edges_data: list, path: Path) -> Dict[str, Any]:
    current_node = path[-1]
    return {
        (dst if src == current_node else src): data["cost"]
        for src, dst, data in edges_data
        if src == current_node or dst == current_node
    }


# nodes_data = list(nx.Graph.nodes(data=True))
def get_rewards(nodes_data: list, path: Path) -> Dict[str, Any]:
    rewards = {node: data["reward"] for node, data in nodes_data if node != path[-1]}
    rewards.update({node: 0 for node in rewards.keys() if node in path})
    return rewards


# nodes_data = list(nx.Graph.nodes(data=True))
def get_random_path(nodes_data: list, number_of_nodes: int) -> Path:
    nodes = []
    for _ in range(number_of_nodes):
        node = random.choice([n for n in nodes_data[1:] if not nodes or n != nodes[-1]])
        nodes.append(node)
    return Path(["P"] + [node for node, data in nodes] + ["P"])


# SA


def replace_one_node(
    nodes_data: list,
    path: Path,
    excluded_indexes: list[int] = [],
    node_to_replace: int = None,
) -> Path:
    new_path = deepcopy(path)  # maybe not necessary here [?]
    if not node_to_replace:
        valid_indexes = [
            i for i in range(1, len(new_path) - 2) if i not in excluded_indexes
        ]
        if not valid_indexes:
            return new_path
        node_to_replace = random.choice(valid_indexes)

    old_node = new_path[node_to_replace]
    node_names = [node for node, _ in nodes_data[1:]]
    possible_nodes = [
        n
        for n in node_names
        if n != old_node
        and n != new_path[node_to_replace - 1]
        and n != new_path[node_to_replace + 1]
    ]
    if not possible_nodes:
        return new_path

    new_path[node_to_replace] = random.choice(possible_nodes)

    return new_path


def replace_n_nodes(nodes_data: list, path: Path, n: int) -> Path:
    if n > len(path) - 2:
        n = len(path) - 2  # to avoid errors
    replaced_indexes = set()
    new_path = deepcopy(path)

    for _ in range(n):
        new_path = replace_one_node(nodes_data, new_path, list(replaced_indexes))
        for i in range(1, len(path) - 1):
            if path[i] != new_path[i] and i not in replaced_indexes:
                replaced_indexes.add(i)
                break

    return new_path


def reverse_fragment(nodes_data: list, path: Path, frag_len: int) -> Path:
    if frag_len < 2 or frag_len > len(path) - 2:
        return path

    start_idx = random.randint(1, len(path) - frag_len - 1)
    end_idx = start_idx + frag_len

    new_path = deepcopy(path)
    new_path[start_idx:end_idx] = reversed(new_path[start_idx:end_idx])

    return new_path


def verify_path(nodes_data: list, path: Path) -> Path:
    for i in range(1, len(path) - 2):
        if path[i] == path[i + 1]:
            path = replace_one_node(nodes_data, path, node_to_replace=i)
    return path


# nodes_data = list(nx.Graph.nodes(data=True))
def mutate_path(nodes_data: list, path: Path, mutation_strength: float):
    new_path = deepcopy(path)

    # replace nodes
    if random.uniform(0, 1) < mutation_strength:
        new_path = replace_n_nodes(
            nodes_data, new_path, int(mutation_strength * (len(path) - 2))
        )

    # reverse fragment
    if random.uniform(0, 1) < mutation_strength:
        new_path = reverse_fragment(
            nodes_data, new_path, int(mutation_strength * (len(path) - 2))
        )

    new_path = verify_path(nodes_data, new_path)

    return new_path


# A*


# nodes_data = list(nx.Graph.nodes(data=True))
def find_n_best_nodes(nodes_data: list, n: int) -> list:
    node_rewards = {node: data["reward"] for node, data in nodes_data if node != "P"}
    sorted_nodes = sorted(
        node_rewards.items(), key=lambda item: item[1], reverse=True
    )  # best first
    best_nodes = [node for node in sorted_nodes[:n]]
    return best_nodes


# edges_data = list(nx.Graph.edges(data=True))
def find_n_best_edges(edges_data: list, n: int) -> list:
    edge_costs = {(src, dst): data["cost"] for src, dst, data in edges_data}
    sorted_edges = sorted(edge_costs.items(), key=lambda item: item[1])  # best first
    best_edges = [edge for edge in sorted_edges[: n + 1]]
    return best_edges


def calc_best_theoretical_objective(
    graph: nx.Graph, best_nodes: list, best_edges: list, path: Path
) -> float:
    edges_in_path = [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]

    current_edges_set = set()
    for edge in edges_in_path:
        current_edges_set.add(edge)
        current_edges_set.add((edge[1], edge[0]))
    available_best_edges = []
    for edge, cost in best_edges:
        if (
            edge not in current_edges_set
            and (edge[1], edge[0]) not in current_edges_set
        ):
            available_best_edges.append((edge, cost))

    available_best_nodes = []
    for node, reward in best_nodes:
        if node not in path:
            available_best_nodes.append((node, reward))

    total_reward = sum(graph.nodes[node]["reward"] for node in path)
    nodes_to_add = len(best_nodes) - len(path)
    for i in range(nodes_to_add):
        total_reward += available_best_nodes[i][1]
    total_cost = sum(graph[u][v]["cost"] for u, v in edges_in_path)
    edges_to_add = len(best_edges) - len(edges_in_path)
    for i in range(edges_to_add):
        total_cost += available_best_edges[i][1]

    return total_reward / total_cost
