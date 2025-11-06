import networkx as nx
from path import Path


def objective_function(graph: nx.Graph, path: Path) -> float:
    rewards = sum(
        graph.nodes[node]["reward"] for node in set(path) if node in graph.nodes
    )
    # costs = sum(graph[u][v]["cost"] for u, v in zip(path[:-1], path[1:]))
    costs = 0
    for u, v in zip(path[:-1], path[1:]):
        edge_cost = graph[u][v]["cost"]
        costs += edge_cost
        # 👇 tu możesz postawić breakpoint
        # print(f"Debug: {u} -> {v}, cost={edge_cost}")

    return rewards / costs
