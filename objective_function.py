import networkx as nx

from models.path import Path


def objective_function(graph: nx.Graph, path: Path) -> float:
    rewards = sum(graph.nodes[node]["reward"] for node in set(path))
    # costs = sum(graph[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
    costs = 0
    for u, v in zip(path[:-1], path[1:], strict=False):
        edge_cost = graph[u][v]["cost"]
        costs += edge_cost

    return rewards / costs
