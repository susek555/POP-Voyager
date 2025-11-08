import math
import random
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

import networkx as nx
import numpy as np

import utils.sa
from models.graph import NodesData
from models.path import Path
from utils.sa import SAparams


def SA(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: SAparams,
) -> Path:
    nodes_data: NodesData = list(graph.nodes(data=True))
    best_path = utils.get_random_path(nodes_data, max_nodes)
    best_eval = objective_function(graph, best_path)
    current_path, current_eval = best_path, best_eval
    scores = [best_eval]

    for i in range(params.n_iter):
        # temp = params.start_temp * (params.n_iter - i + 1) / params.n_iter
        # temp = params.start_temp * (params.decrease_factor**i)
        # temp = params.start_temp / math.log(1 + i)
        # temp = max(params.start_temp / 2, params.start_temp / math.log(2 + i))
        temp = params.start_temp - (params.start_temp / 2 * i / params.n_iter)

        mutation_strength = temp / params.start_temp

        def evaluate_candidate(c):
            return objective_function(graph, c)

        with ThreadPoolExecutor(max_workers=params.n_threads) as executor:
            candidates = [
                utils.sa.mutate_path(nodes_data, current_path, mutation_strength)
                for _ in range(params.n_candidates_per_thread)
            ]
            evaluations = list(executor.map(evaluate_candidate, candidates))

        best_candidate_idx = np.argmax(evaluations)
        candidate_path = candidates[best_candidate_idx]
        candidate_eval = evaluations[best_candidate_idx]

        if candidate_eval > best_eval or random.random() < math.exp(
            (candidate_eval - current_eval) / temp
        ):
            current_path, current_eval = candidate_path, candidate_eval
            if candidate_eval > best_eval:
                best_path, best_eval = candidate_path, candidate_eval
                scores.append(best_eval)

        if i % (params.n_iter / 10) == 0:
            print(f"Iteration {i}, Temperature {temp:.3f}, Best Evaluation {best_eval:.5f}")

    return best_path
