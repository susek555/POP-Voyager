from collections.abc import Callable

import networkx as nx

import utils
import utils.ant_colony
from models.path import Path
from utils.ant_colony import AcoParams


def aco(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: AcoParams,
) -> Path:
    best_path: Path | None = None
    best_score: float = float("-inf")

    graph = utils.ant_colony.init_pheromone_graph(graph, params.default_pheromone)

    candidate_lists: dict[str, set[str]] | None = None
    k = params.candidate_list_size
    if k and k > 0:
        candidate_lists = utils.ant_colony.generate_candidate_list(graph, k)

    for _iteration in range(params.iteration_count):
        iteration_paths = []

        for _ant in range(params.ant_count):
            path = utils.ant_colony.construct_ant_path(graph, max_nodes, params, candidate_lists)
            score = objective_function(graph, path)
            iteration_paths.append((path, score))

        utils.ant_colony.evaporate_pheromones(graph, params.pheromone_degradation_rate)

        for path, score in iteration_paths:
            if score > best_score:
                best_score = score
                best_path = path

            if score > 0:
                utils.ant_colony.deposit_pheromones(graph, path, score, params.Q)

        if best_path is not None and best_score > 0:
            utils.ant_colony.deposit_pheromones(
                graph, best_path, best_score, params.Q * params.elite_factor
            )

        if _iteration % 10 == 0:
            logger.info(f"ACO best path: {best_score}")

    return best_path if best_path is not None else Path(["P", "P"])
