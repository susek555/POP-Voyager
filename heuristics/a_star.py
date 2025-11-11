import networkx as nx

import utils.a_star
from models.path import Path
from utils.logger import logger

# def a_star(
#     graph: nx.Graph,
#     max_nodes: int,
# ) -> Path:
#     nodes_data = list(graph.nodes(data=True))
#     edges_data = list(graph.edges(data=True))
#     start_end_node = "P"
#     best_nodes = utils.a_star.find_n_best_nodes(nodes_data, max_nodes)
#     best_edges = utils.a_star.find_n_best_edges(edges_data, max_nodes + 1)
#     start_path = Path(["P"])
#     best_eval, best_path = 0, None
#     decider = 1

#     search_queue = []
#     heapq.heappush(
#         search_queue,
#         (
#             -(utils.a_star.calc_best_theoretical_objective(graph, best_nodes, best_edges, start_path)),
#             decider,
#             start_path,
#         )
#     )

#     while search_queue:
#         neg_eval, _, current_path = heapq.heappop(search_queue)
#         current_eval = -neg_eval

#         if len(current_path) == max_nodes + 1:
#             current_path += start_end_node
#             current_eval = utils.a_star.calc_best_theoretical_objective(
#                 graph, best_nodes, best_edges, current_path
#             )
#             if current_eval > best_eval:
#                 best_eval = current_eval
#                 best_path = current_path
#                 logger.info(f"New best = {best_eval:.4f}")
#             continue
#         else:
#             children = utils.a_star.get_children(nodes_data, current_path)
#             for child in children:
#                 child_eval = utils.a_star.calc_best_theoretical_objective(
#                     graph, best_nodes, best_edges, child
#                 )
#                 if child_eval > best_eval:
#                     decider += 1
#                     heapq.heappush(search_queue, (-child_eval, decider, child))

#     return best_path or Path(["P", "P"])


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

    iteration = 0
    logger.info(f"Max theoretical objective = {utils.a_star.calc_best_theoretical_objective(
                graph, best_nodes, best_edges, start_path
            )}")

    search_stack = [start_path]

    while search_stack:
        current_path = search_stack.pop()

        if len(current_path) == max_nodes + 1:
            current_path += start_end_node
            current_eval = utils.a_star.calc_best_theoretical_objective(
                graph, best_nodes, best_edges, current_path
            )
            if current_eval > best_eval:
                best_eval = current_eval
                best_path = current_path
                logger.info(f"New best = {best_eval:.4f}")
            continue
        else:
            children = utils.a_star.get_children(nodes_data, current_path)

            scored_children = []
            for child in children:
                current_eval = utils.a_star.calc_best_theoretical_objective(
                    graph, best_nodes, best_edges, child
                )

                if current_eval < best_eval:
                    continue

                scored_children.append((current_eval, child))

            scored_children.sort(key=lambda x: -x[0], reverse=True)

            for _, child in scored_children:
                search_stack.append(child)

        iteration += 1
        if iteration % 10000 == 0:
            logger.info(f"Elements on stack = {len(search_stack)}, Current eval = {current_eval}")

    return best_path or Path(["P", "P"])
