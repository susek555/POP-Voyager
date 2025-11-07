<<<<<<< HEAD
=======
import networkx as nx
import genetic_utils
from path import Path
import random
from typing import Callable
import heuristics_utils
>>>>>>> 7f73ae3 (implement genetic algorithm)
import math
import random
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue
from typing import Callable

import networkx as nx
import numpy as np

import genetic_utils
import heuristics_utils
from graph_types import EdgesData, NodesData
from path import Path

from graph_types import NodesData, EdgesData


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
    nodes_data: NodesData = list(graph.nodes(data=True))
    edges_data: EdgesData = list(graph.edges(data=True))
    path = Path(["P"])

    for i in range(0, max_nodes):
        costs = heuristics_utils.get_costs_from_node(edges_data, path)
        rewards = heuristics_utils.get_rewards(nodes_data, path)

        ratios = {node: rewards[node] / costs[node] for node in rewards if node in costs}

        next_node = max(ratios, key=ratios.get)
        path += next_node

    return path + "P"


def SA(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: heuristics_utils.SAparams,
) -> Path:
    nodes_data: NodesData = list(graph.nodes(data=True))
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
                heuristics_utils.mutate_path(nodes_data, current_path, mutation_strength)
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


<<<<<<< HEAD
def A_star(
    graph: nx.Graph,
    max_nodes: int,
):
    nodes_data = list(graph.nodes(data=True))
    edges_data = list(graph.edges(data=True))
    start_end_node = "P"
    best_nodes = heuristics_utils.find_n_best_nodes(nodes_data, max_nodes)
    best_edges = heuristics_utils.find_n_best_edges(edges_data, max_nodes + 1)
    start_path = Path(["P"])
    best_eval, best_path = 0, None

    search_queue = PriorityQueue()
    search_queue.put(
        (
            heuristics_utils.calc_best_theoretical_objective(
                graph, best_nodes, best_edges, start_path
            ),
            random.random(),
            start_path,
        )
    )

    while not search_queue.empty():
        current_eval, _, current_path = search_queue.get()

        if len(current_path) == max_nodes + 1:
            current_path += start_end_node
            current_eval = heuristics_utils.calc_best_theoretical_objective(
                graph, best_nodes, best_edges, current_path
            )
            if current_eval > best_eval:
                best_eval = current_eval
                best_path = current_path
            continue
        else:
            children = heuristics_utils.get_children(nodes_data, current_path)
            for child in children:
                child_eval = heuristics_utils.calc_best_theoretical_objective(
                    graph, best_nodes, best_edges, child
                )
                if child_eval > best_eval:
                    search_queue.put((child_eval, random.random(), child))

    return best_path

=======
>>>>>>> 7f73ae3 (implement genetic algorithm)
def genetic(
    graph: nx.Graph,
    objective_function: Callable[[nx.Graph, Path], float],
    max_nodes: int,
    params: genetic_utils.GeneticParams,
) -> Path:
    nodes_data: NodesData = list(graph.nodes(data=True))
    population: list[Path] = [
        genetic_utils.get_random_path_no_duplicates(nodes_data, max_nodes)
        for _ in range(params.pop_size)
    ]
    fitness = [objective_function(graph, path) for path in population]

    no_change_count: int = 0

    best_path, best_score = genetic_utils.get_best_path_info(population, fitness)

    for _ in range(params.generations):
        if params.no_improvement_stop and no_change_count > params.no_improvement_stop:
            print("Ending early")
            break

        new_population: list[Path] = []

        while len(new_population) < params.pop_size:
            parent1 = params.selection(population, fitness, **params.selection_kwargs)
            parent2 = params.selection(population, fitness, **params.selection_kwargs)

            child1, child2 = params.crossover(parent1, parent2)

            if random.random() < params.mutation_rate:
                genetic_utils.mutate(child1)
            if random.random() < params.mutation_rate:
                genetic_utils.mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[: params.pop_size]
        fitness = [objective_function(graph, path) for path in population]
        gen_best_path, gen_best_score = genetic_utils.get_best_path_info(population, fitness)

        if gen_best_score > best_score:
            best_score = gen_best_score
            best_path = gen_best_path
        else:
            no_change_count += 1

    return best_path
