import networkx as nx
import draw_graph
import generate_graph

# Tworzymy graf
G = generate_graph.generate_graph(
    number_of_nodes=10,
    # max_base_distance=10.0,
    # reward_range=(5, 20),
    # cost_factor=1.0
)

draw_graph.draw_graph(G, "Example 3D Graph")
