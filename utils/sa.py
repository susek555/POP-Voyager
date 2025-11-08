import random
from copy import deepcopy
from dataclasses import dataclass

from models.graph import NodesData
from models.path import Path


@dataclass
class SAparams:
    n_iter: int
    start_temp: float
    decrease_factor: float
    n_threads: int
    n_candidates_per_thread: int


def replace_one_node(
    nodes_data: NodesData,
    path: Path,
    excluded_indexes: list[int] | None = None,
    node_to_replace: int | None = None,
) -> Path:
    if excluded_indexes is None:
        excluded_indexes = []

    new_path = deepcopy(path)  # maybe not necessary here [?]
    if not node_to_replace:
        valid_indexes = [i for i in range(1, len(new_path) - 2) if i not in excluded_indexes]
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


def replace_n_nodes(nodes_data: NodesData, path: Path, n: int) -> Path:
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


def reverse_fragment(nodes_data: NodesData, path: Path, frag_len: int) -> Path:
    if frag_len < 2 or frag_len > len(path) - 2:
        return path

    start_idx = random.randint(1, len(path) - frag_len - 1)
    end_idx = start_idx + frag_len

    new_path = deepcopy(path)
    new_path[start_idx:end_idx] = list(reversed(new_path[start_idx:end_idx]))

    return new_path


def verify_path(nodes_data: NodesData, path: Path) -> Path:
    for i in range(1, len(path) - 2):
        if path[i] == path[i + 1]:
            path = replace_one_node(nodes_data, path, node_to_replace=i)
    return path


def mutate_path(nodes_data: NodesData, path: Path, mutation_strength: float) -> Path:
    new_path = deepcopy(path)

    # replace nodes
    if random.uniform(0, 1) < mutation_strength:
        new_path = replace_n_nodes(nodes_data, new_path, int(mutation_strength * (len(path) - 2)))

    # reverse fragment
    if random.uniform(0, 1) < mutation_strength:
        new_path = reverse_fragment(nodes_data, new_path, int(mutation_strength * (len(path) - 2)))

    new_path = verify_path(nodes_data, new_path)

    return new_path
