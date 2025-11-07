import networkx as nx
from path import Path
import random
from typing import Callable
import heuristics_utils
import math
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def full_random(graph: nx.Graph, max_nodes: int) -> Path:
    path = Path(["P"])
    nodes = list(graph.nodes())
    nodes.remove("P")
    for i in range(0, max_nodes):
        chosen_node = random.choice(nodes)
        path += chosen_node
        nodes.remove(chosen_node)
    return path + "P"


def greedy(graph: nx.Graph, max_nodes: int) -> Path:
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    path = Path(["P"])

    for i in range(0, max_nodes):
        costs = heuristics_utils.get_costs_from_node(edges_data, path)
        rewards = heuristics_utils.get_rewards(nodes_data, path)

        ratios = {
            node: rewards[node] / costs[node] for node in rewards if node in costs
        }

        next_node = max(ratios, key=ratios.get)
        path += next_node

    return path + "P"


def SA(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: heuristics_utils.SAparams,
) -> Path:
    nodes_data = list(graph.nodes(data=True))
    # edges_data = list(graph.edges(data=True))
    best_path = heuristics_utils.get_random_path(nodes_data, max_nodes)
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
                heuristics_utils.mutate_path(
                    nodes_data, current_path, mutation_strength
                )
                for _ in range(params.n_candidates_per_thread)
            ]
            evaluations = list(executor.map(evaluate_candidate, candidates))

        best_candidate_idx = np.argmax(evaluations)
        candidate_path = candidates[best_candidate_idx]
        candidate_eval = evaluations[best_candidate_idx]

        # candidate_path = heuristics_utils.mutate_path(
        #     nodes_data, current_path, mutation_strength
        # )
        # # candidate_path = heuristics_utils.replace_one_node(nodes_data, current_path)
        # candidate_eval = objective_function(graph, candidate_path)

        if candidate_eval > best_eval or random.random() < math.exp(
            (candidate_eval - current_eval) / temp
        ):
            current_path, current_eval = candidate_path, candidate_eval
            if candidate_eval > best_eval:
                best_path, best_eval = candidate_path, candidate_eval
                scores.append(best_eval)

        if i % (params.n_iter / 10) == 0:
            print(
                f"Iteration {i}, Temperature {temp:.3f}, Best Evaluation {best_eval:.5f}"
            )

    return best_path
