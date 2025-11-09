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
    number_of_nodes=500,
    max_base_distance=100.0,
    reward_range=(10, 100),
    cost_factor=0.5,
)

path = full_random(G, 100)
print(f"Random: {objective_function(G, path)}")
path = greedy(G, 100)
print(f"Greedy: {objective_function(G, path)}")
path = genetic(
    G,
    objective_function,
    100,
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
path = aco(
    G,
    objective_function,
    100,
    AcoParams(
        ant_count=80,
        iteration_count=600,
        alpha=1,
        beta=2,
        pheromone_degradation_rate=0.1,
        Q=300,
        candidate_list_size=60,
    ),
)
print(f"ACO: {objective_function(G, path)}")

path = a_star(G, 100)
print(f"A_star: {objective_function(G, path)}")


# draw_graph(G, "Example 3D Graph", path)
