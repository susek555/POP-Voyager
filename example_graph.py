import networkx as nx
import draw_graph
import generate_graph
from objective_function import objective_function
import heuristics
from heuristics_utils import SAparams

G = generate_graph.generate_graph(
    number_of_nodes=20,
    max_base_distance=50.0,
    # reward_range=(5, 20),
    cost_factor=0.2,
)

# path = Path(['P', 's1', 's2', 's3', 'P'])
path = heuristics.full_random(G, 6)
print(f"Random: {objective_function(G, path)}")
path = heuristics.greedy(G, 6)
print(f"Greedy: {objective_function(G, path)}")
path = heuristics.SA(G, objective_function, 6, SAparams(1000, 50, 0.99))

# TODO SA need more exploration
# add dynamic metric of what % of nodes replace randomly per iteration

print(f"SA: {objective_function(G, path)}")


# draw_graph.draw_graph(G, "Example 3D Graph", path)
