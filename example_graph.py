import generate_graph
import heuristics
from objective_function import objective_function
from utils.ant_colony import AcoParams
from utils.genetic import GeneticParams, ordered_crossover, select_tournament
from utils.sa import SAparams

G = generate_graph.generate_graph(
    number_of_nodes=20,
    max_base_distance=50.0,
    reward_range=(10, 40),
    cost_factor=0.2,
)

path = heuristics.full_random(G, 6)
print(f"Random: {objective_function(G, path)}")
path = heuristics.greedy(G, 6)
print(f"Greedy: {objective_function(G, path)}")
path = heuristics.SA(G, objective_function, 6, SAparams(1000, 500, 0.995, 4, 4))
print(f"SA: {objective_function(G, path)}")
path = heuristics.genetic(
    G,
    objective_function,
    6,
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
path = heuristics.aco(
    G,
    objective_function,
    6,
    AcoParams(
        ant_count=20,
        iteration_count=100,
        alpha=0.8,
        beta=1.5,
        pheromone_degradation_rate=0.1,
        Q=100,
    ),
)
print(f"ACO: {objective_function(G, path)}")

path = heuristics.A_star(G, 6)
print(f"A_star: {objective_function(G, path)}")


# draw_graph.draw_graph(G, "Example 3D Graph", path)
