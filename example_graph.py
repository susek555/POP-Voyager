import networkx as nx
import draw_graph
import generate_graph
from target_function import target_function
from path import Path

# Tworzymy graf
G = generate_graph.generate_graph(
    number_of_nodes=10,
    max_base_distance=50.0,
    # reward_range=(5, 20),
    cost_factor=0.2
)

path = Path(['P', 's1', 's2', 's3', 'P'])
print(target_function(G, path.path))


draw_graph.draw_graph(G, "Example 3D Graph", path)
