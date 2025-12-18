import logging
import random
from collections.abc import Callable

import networkx as nx

import utils.genetic
from models.graph import NodesData
from models.path import Path
from utils.genetic import GeneticParams

logger = logging.getLogger(__name__)


def genetic(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: GeneticParams,
) -> Path:
    nodes_data: NodesData = list(graph.nodes(data=True))
    population: list[Path] = [
        utils.genetic.get_random_path_no_duplicates(nodes_data, max_nodes)
        for _ in range(params.pop_size)
    ]
    fitness = [objective_function(graph, path) for path in population]

    no_change_count: int = 0

    best_path, best_score = utils.genetic.get_best_path_info(population, fitness)

    for _ in range(params.generations):
        if params.no_improvement_stop and no_change_count > params.no_improvement_stop:
            logger.info("Ending early")
            break

        new_population: list[Path] = []

        elite_path, _ = utils.genetic.get_best_path_info(population, fitness)
        new_population.append(Path(list(elite_path)))

        while len(new_population) < params.pop_size:
            parent1 = params.selection(population, fitness, **params.selection_kwargs)
            parent2 = params.selection(population, fitness, **params.selection_kwargs)

            child1, child2 = params.crossover(parent1, parent2)

            if random.random() < params.mutation_rate:
                utils.genetic.mutate(child1)
            if random.random() < params.mutation_rate:
                utils.genetic.mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[: params.pop_size]
        fitness = [objective_function(graph, path) for path in population]
        gen_best_path, gen_best_score = utils.genetic.get_best_path_info(population, fitness)

        if gen_best_score > best_score:
            best_score = gen_best_score
            best_path = gen_best_path
            no_change_count = 0
        else:
            no_change_count += 1

    return best_path
