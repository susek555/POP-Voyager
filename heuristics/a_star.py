import random
from queue import PriorityQueue

import networkx as nx

import utils.a_star
from models.path import Path


def a_star(
    graph: nx.Graph,
    max_nodes: int,
) -> Path:
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    start_end_node = "P"
    best_nodes = utils.a_star.find_n_best_nodes(nodes_data, max_nodes)
    best_edges = utils.a_star.find_n_best_edges(edges_data, max_nodes + 1)
    start_path = Path(["P"])
    best_eval, best_path = 0, None

    search_queue = PriorityQueue()
    search_queue.put(
        (
            utils.a_star.calc_best_theoretical_objective(graph, best_nodes, best_edges, start_path),
            random.random(),
            start_path,
        )
    )

    while not search_queue.empty():
        current_eval, _, current_path = search_queue.get()

        if len(current_path) == max_nodes + 1:
            current_path += start_end_node
            current_eval = utils.a_star.calc_best_theoretical_objective(
                graph, best_nodes, best_edges, current_path
            )
            if current_eval > best_eval:
                best_eval = current_eval
                best_path = current_path
            continue
        else:
            children = utils.a_star.get_children(nodes_data, current_path)
            for child in children:
                child_eval = utils.a_star.calc_best_theoretical_objective(
                    graph, best_nodes, best_edges, child
                )
                if child_eval > best_eval:
                    search_queue.put((child_eval, random.random(), child))

    return best_path or Path(["P", "P"])
