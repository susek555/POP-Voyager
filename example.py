import utils
import utils.ant_colony
import utils.ant_colony.stagnation_strategies
from graph.generate import generate_graph
from heuristics.a_star import a_star
from heuristics.ant_colony import aco
from heuristics.genetic import genetic
from heuristics.greedy import greedy
from heuristics.random import full_random
from objective_function import objective_function
from utils.ant_colony.common import AcoParams
from utils.genetic import GeneticParams, ordered_crossover, select_tournament

# Disable <= CRITICAL logs from imported functions
# logging.disable(logging.CRITICAL)

G = generate_graph(
    number_of_nodes=50,
    max_base_distance=100.0,
    reward_range=(10, 100),
    cost_factor=0.2,
)

path = full_random(G, 20)
print(f"Random: {objective_function(G, path)}")
path = greedy(G, 20)
print(f"Greedy: {objective_function(G, path)}")
path = genetic(
    G,
    objective_function,
    20,
    GeneticParams(
        pop_size=30,
        generations=100,
        mutation_rate=0.05,
        crossover=ordered_crossover,
        selection=select_tournament,
        selection_kwargs={"tournament_size": 4},
    ),
)
print(f"Genetic: {objective_function(G, path)}")
# path = aco(
#     G,
#     objective_function,
#     20,
#     AcoParams(
#         ant_count=100,
#         iteration_count=400,
#         alpha=1,
#         beta=2,
#         pheromone_degradation_rate=0.1,
#         Q=300,
#         candidate_list_size=60,
#     ),
#     stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
# )
# print(f"ACO: {objective_function(G, path)}")
# path = aco(
#     G,
#     objective_function,
#     20,
#     AcoParams(
#         ant_count=100,
#         iteration_count=400,
#         alpha=1.5,
#         beta=2.5,
#         pheromone_degradation_rate=0.15,
#         Q=300,
#         candidate_list_size=60,
#         deposit_mode="diffusion",
#         diffusion_range=1,
#     ),
#     stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
# )
# print(f"ACO (diffused): {objective_function(G, path)}")

path = a_star(G, 20)
print(f"A_star: {objective_function(G, path)}")

# draw_graph(G, "Example 3D Graph", path)
