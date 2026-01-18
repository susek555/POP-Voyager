import logging
import random
from collections.abc import Callable

import networkx as nx

import utils.ant_colony.common as ant_colony
import utils.ant_colony.stagnation_strategies as ant_colony_strategies
from models.path import Path

logger = logging.getLogger(__name__)


def aco(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: ant_colony.AcoParams,
    stagnation_strategy: ant_colony_strategies.StagnationStrategy | None = None,
) -> Path:
    rng = random.Random(params.seed)
    if stagnation_strategy is None:
        stagnation_strategy = ant_colony_strategies.NoStrategy()

    state = ant_colony.AcoState(
        iteration=0,
        best_score=float("-inf"),
        best_path=None,
        iteration_paths=[],
        no_improvement_count=0,
        graph=ant_colony.init_pheromone_graph(graph, params.default_pheromone),
    )

    candidate_lists: dict[str, set[str]] | None = None
    k = params.candidate_list_size
    if k and k > 0:
        candidate_lists = ant_colony.generate_candidate_list(state.graph, k)

    for iteration in range(params.iteration_count):
        state.iteration = iteration
        state.iteration_paths = []

        for _ in range(params.ant_count):
            path = ant_colony.construct_ant_path(
                state.graph, max_nodes, params, candidate_lists, rng
            )
            score = objective_function(state.graph, path)
            state.iteration_paths.append((path, score))

        ant_colony.evaporate_pheromones(state.graph, params.pheromone_degradation_rate)

        new_best: bool = False
        for path, score in state.iteration_paths:
            if score > state.best_score:
                state.best_score = score
                state.best_path = path
                new_best = True
                state.no_improvement_count = 0

            if score < 0:
                continue

            if params.deposit_mode == "standard":
                ant_colony.deposit_pheromones(
                    state.graph,
                    path,
                    score,
                    params.Q,
                )
            elif params.deposit_mode == "diffusion":
                ant_colony.deposit_pheromones_with_diffusion(
                    state.graph,
                    path,
                    score,
                    params.Q,
                    candidate_lists=candidate_lists,
                    diffusion_range=params.diffusion_range,
                )

        if new_best:
            logger.info(f"Iter {iteration:3d}: New best = {state.best_score:.4f}")
        else:
            state.no_improvement_count += 1

        if state.best_path is not None and state.best_score > 0:
            if params.deposit_mode == "standard":
                ant_colony.deposit_pheromones(
                    state.graph,
                    state.best_path,
                    state.best_score,
                    params.Q * params.elite_factor,
                )
            elif params.deposit_mode == "diffusion":
                ant_colony.deposit_pheromones_with_diffusion(
                    state.graph,
                    state.best_path,
                    state.best_score,
                    params.Q,
                    candidate_lists=candidate_lists,
                    diffusion_range=params.diffusion_range,
                )

        if stagnation_strategy.should_act(state):
            stagnation_strategy.execute(state, params)

        should_stop, reason = stagnation_strategy.should_stop(state)
        if should_stop:
            logger.info(f"Iter {iteration:3d}: {reason}")
            break

    return state.best_path if state.best_path is not None else Path(["P", "P"])
