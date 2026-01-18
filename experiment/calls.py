from collections.abc import Callable

import networkx as nx

from graph.config import Graph, GraphScenario
from models.path import Path
from utils.config import Algorithm, AlgorithmType


def call_algorithm(
    algorithm: Algorithm,
    graph: nx.Graph,
    max_nodes: int,
    objective_function: Callable[[nx.Graph, Path], float],
    seed: int,
) -> Path:
    algorithm.params.seed = seed

    if algorithm.type == AlgorithmType.RANDOM:
        from heuristics.random import full_random

        return full_random(graph, max_nodes)
    elif algorithm.type == AlgorithmType.GREEDY:
        from heuristics.greedy import greedy

        return greedy(graph, max_nodes)
    elif algorithm.type == AlgorithmType.SA:
        from heuristics.sa import SA

        return SA(graph, objective_function, max_nodes, algorithm.params)
    elif algorithm.type == AlgorithmType.GENETIC:
        from heuristics.genetic import genetic

        return genetic(graph, objective_function, max_nodes, algorithm.params)
    elif algorithm.type == AlgorithmType.ACO:
        from heuristics.ant_colony import aco

        return aco(graph, objective_function, max_nodes, algorithm.params)
    elif algorithm.type == AlgorithmType.A_STAR:
        from heuristics.a_star import A_star

        return A_star(graph, max_nodes, algorithm.params)
    else:
        raise ValueError(f"Unknown algorithm type: {algorithm.type}")


def call_generate_graph(graph: Graph, seed: int) -> nx.Graph:
    graph.params.seed = seed

    if graph.scenario == GraphScenario.BASIC:
        from graph.generate import generate_graph

        return generate_graph(graph.params)
    elif graph.scenario == GraphScenario.ARCHIPELAGO:
        from graph.scenarios.archipelago import generate_archipelago_graph

        return generate_archipelago_graph(graph.params)
    elif graph.scenario == GraphScenario.BOTTLENECK:
        from graph.scenarios.bottleneck import generate_bottleneck_graph

        return generate_bottleneck_graph(graph.params)
    elif graph.scenario == GraphScenario.GRADIENT:
        from graph.scenarios.gradient import generate_gradient_graph

        return generate_gradient_graph(graph.params)
    elif graph.scenario == GraphScenario.LINE_CIRCLE:
        from graph.scenarios.line_circle import generate_line_circle_graph

        return generate_line_circle_graph(graph.params)
    elif graph.scenario == GraphScenario.NEBULA:
        from graph.scenarios.nebula import generate_nebula_graph

        return generate_nebula_graph(graph.params)
    elif graph.scenario == GraphScenario.SIREN_SONG:
        from graph.scenarios.siren_song import generate_siren_song_graph

        return generate_siren_song_graph(graph.params)
    else:
        raise ValueError(f"Unknown graph scenario: {graph.scenario}")
