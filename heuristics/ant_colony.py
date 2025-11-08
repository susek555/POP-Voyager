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

    for _iteration in range(params.iteration_count):
        iteration_paths = []

        for _ant in range(params.ant_count):
            path = utils.ant_colony.construct_ant_path(graph, max_nodes, params)
            score = objective_function(graph, path)
            iteration_paths.append((path, score))

            if score > best_score:
                best_score = score
                best_path = path

        utils.ant_colony.evaporate_pheromones(graph, params.pheromone_degradation_rate)

        for path, score in iteration_paths:
            if score > 0:
                utils.ant_colony.deposit_pheromones(graph, path, score, params.Q)

        if _iteration % 10 == 0:
            print(f"ACO best path: {best_score}")

    return best_path if best_path is not None else Path(["P", "P"])
