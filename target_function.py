import networkx as nx
from path import Path


def target_function(graph: nx.Graph, path: Path) -> float:
    rewards = sum(
        data["reward"] for (node, data) in graph.nodes(data=True) if node in path
    )
    costs = sum(graph[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
    return rewards / costs
