import logging

import utils.ant_colony.stagnation_strategies
from graph.draw import draw_graph
from graph.generate import generate_graph
from graph.generate_return_trap import generate_trap_graph
from heuristics.a_star import A_star
from heuristics.ant_colony import aco
from heuristics.genetic import genetic
from heuristics.greedy import greedy
from heuristics.random import full_random
from heuristics.sa import SA
from objective_function import objective_function
from utils.a_star import ChildrenFactory
from utils.ant_colony.common import AcoParams
from utils.genetic import GeneticParams, ordered_crossover, select_tournament
from utils.logger import setup_logger
from utils.sa import SAparams

setup_logger(logging.INFO)
# Disable <= CRITICAL logs from imported functions
# logging.disable(logging.CRITICAL)

# G = generate_graph(
#     number_of_nodes=15,
#     max_base_distance=100.0,
#     reward_range=(10, 100),
#     cost_factor=0.2,
# )
G = generate_trap_graph(
    n_nodes_line=10,
    n_nodes_circle=20,
    line_dist=1.0,
    circle_radius=500.0,
    reward_range=(10, 100),
    cost_factor=0.6,
    circle_multiplier=100.0,
)

paths = {}
evals = {}

path = full_random(G, 10)
print(f"Random: {objective_function(G, path)}")
paths["Random"] = path
evals["Random"] = objective_function(G, path)

path = greedy(G, 10)
print(f"Greedy: {objective_function(G, path)}")
greedy_eval = objective_function(G, path)
paths["Greedy"] = path
evals["Greedy"] = objective_function(G, path)

path = SA(
    G,
    objective_function,
    10,
    SAparams(
        n_iter=5000,
        start_temp=100.0,
        decrease_factor=0.99,
        n_threads=4,
        n_candidates_per_thread=4,
    ),
)
print(f"SA: {objective_function(G, path)}")
paths["SA"] = path
evals["SA"] = objective_function(G, path)

path = genetic(
    G,
    objective_function,
    10,
    GeneticParams(
        pop_size=50,
        generations=200,
        mutation_rate=0.15,
        crossover=ordered_crossover,
        selection=select_tournament,
        selection_kwargs={"tournament_size": 3},
    ),
)
print(f"Genetic: {objective_function(G, path)}")
paths["Genetic"] = path
evals["Genetic"] = objective_function(G, path)

path = aco(
    G,
    objective_function,
    10,
    AcoParams(
        ant_count=100,
        iteration_count=400,
        alpha=1,
        beta=2,
        pheromone_degradation_rate=0.1,
        Q=300,
        candidate_list_size=60,
    ),
    stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
)
print(f"ACO: {objective_function(G, path)}")
paths["ACO"] = path
evals["ACO"] = objective_function(G, path)

path = aco(
    G,
    objective_function,
    10,
    AcoParams(
        ant_count=100,
        iteration_count=400,
        alpha=1.5,
        beta=2.5,
        pheromone_degradation_rate=0.15,
        Q=300,
        candidate_list_size=60,
        deposit_mode="diffusion",
        diffusion_range=1,
    ),
    stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
)
print(f"ACO (diffused): {objective_function(G, path)}")
paths["ACO (diffused)"] = path
evals["ACO (diffused)"] = objective_function(G, path)

# path = A_star(G, 10, greedy_eval)
# print(f"A_star: {objective_function(G, path)}")
# path = A_star(G, 10, greedy_eval, childrenFactory=ChildrenFactory.N_BEST, n_children=10)
# print(f"Quazi A_star: {objective_function(G, path)}")
# paths["A*_greedy"] = path
# evals["A*_greedy"] = objective_function(G, path)

draw_graph(G, "Example 3D Graph", paths, evals)
