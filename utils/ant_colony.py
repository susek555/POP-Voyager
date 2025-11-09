import random
from dataclasses import dataclass

import networkx as nx

from models.path import Path


@dataclass
class AcoParams:
    ant_count: int
    iteration_count: int
    alpha: float
    beta: float
    pheromone_degradation_rate: float
    Q: float
    default_pheromone: float = 1e-5
    candidate_list_size: int | None = None
    elite_factor: float = 2.0


def init_pheromone_graph(graph: nx.Graph, pheromone_value: float) -> nx.Graph:
    graph = graph.copy()
    nodes = graph.nodes(data=True)

    for i, (node1, _data1) in enumerate(nodes):
        for j, (node2, _data2) in enumerate(nodes):
            if i < j:
                if graph.has_edge(node1, node2):
                    graph[node1][node2]["pheromone"] = pheromone_value
                else:
                    graph.add_edge(node1, node2, pheromone=pheromone_value)

    return graph


def generate_candidate_list(graph: nx.Graph, size: int) -> dict[str, set[str]]:
    candidate_lists: dict[str, set[str]] = {}
    for node in graph.nodes():
        neighs: list[str] = [n for n in graph.neighbors(node) if n != "P"]
        scored: list[tuple[float, str]] = []
        for n in neighs:
            cost = graph[node][n].get("cost", 1)
            reward = graph.nodes[n].get("reward", 1)
            heuristic = (reward + 1.0) / (cost + 0.1)
            scored.append((heuristic, n))
        scored.sort(reverse=True, key=lambda x: x[0])
        top = {n for _, n in scored[:size]}
        candidate_lists[node] = top

    return candidate_lists


def construct_ant_path(
    graph: nx.Graph,
    max_nodes: int,
    params: AcoParams,
    candidate_lists: dict[str, set[str]] | None = None,
) -> Path:
    current_node = "P"
    path = Path([current_node])
    visited = {current_node}

    while len(path) - 1 < max_nodes:
        neighbors = [
            n
            for n in graph.neighbors(current_node)
            if n not in visited
            and n != "P"
            and (candidate_lists is None or n in candidate_lists[current_node])
        ]

        if not neighbors:
            break

        next_node = select_next_node(graph, current_node, neighbors, params.alpha, params.beta)

        if next_node is None:
            break

        path += next_node
        visited.add(next_node)
        current_node = next_node

    path += "P"

    return path


def select_next_node(
    graph: nx.Graph, current: str, neighbors: list[str], alpha: float, beta: float
) -> str | None:
    if not neighbors:
        return None

    probabilities: list[float] = []

    for neighbor in neighbors:
        edge_data = graph[current][neighbor]

        pheromone: float = edge_data.get("pheromone", 0)

        cost: float = edge_data.get("cost", 1)
        reward: float = graph.nodes[neighbor].get("reward", 1)

        heuristic = (reward + 1.0) / (cost + 0.1)

        prob_component = (pheromone**alpha) * (heuristic**beta)
        probabilities.append(prob_component)

    total = sum(probabilities)
    if total == 0:
        return random.choice(neighbors)

    probabilities = [p / total for p in probabilities]

    selected = random.choices(neighbors, weights=probabilities, k=1)[0]

    return selected


def evaporate_pheromones(graph: nx.Graph, evaporation_rate: float) -> None:
    for _, _, data in graph.edges(data=True):
        current_pheromone = data.get("pheromone", 0)
        data["pheromone"] = (1 - evaporation_rate) * current_pheromone


def deposit_pheromones(graph: nx.Graph, path: Path, score: float, Q: float) -> None:
    if len(path) < 2:
        return

    delta = Q * score

    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if graph.has_edge(u, v):
            graph[u][v]["pheromone"] += delta
