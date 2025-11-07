import networkx as nx
import draw_graph
import generate_graph
from genetic_utils import GeneticParams
import genetic_utils
from objective_function import objective_function
import heuristics
from heuristics_utils import SAparams

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
path = heuristics.SA(G, objective_function, 6, SAparams(10000, 500, 0.995, 4, 4))
print(f"SA: {objective_function(G, path)}")
path = heuristics.genetic(
    G,
    objective_function,
    6,
    GeneticParams(
        pop_size=30,
        generations=100,
        mutation_rate=0.05,
        crossover=genetic_utils.ordered_crossover,
        selection=genetic_utils.select_tournament,
        selection_kwargs={"tournament_size": 4},
    ),
)
print(f"Genetic: {objective_function(G, path)}")

path = heuristics.A_star(G, 6)
print(f"A_star: {objective_function(G, path)}")


# draw_graph.draw_graph(G, "Example 3D Graph", path)
