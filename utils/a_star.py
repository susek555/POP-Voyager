import networkx as nx

from models.graph import EdgesData, NodesData
from models.path import Path


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


def get_children(nodes_data: list, path: Path) -> list[Path]:
    return [path + node for node, _ in nodes_data[1:] if node != path[-1]]
