import networkx as nx
import draw_graph

# Tworzymy graf
G = nx.Graph()

G.add_node("P", reward=0, pos=(0, 0, 0))
G.add_node("s1", reward=15, pos=(1, 2, 0.5))
G.add_node("s2", reward=20, pos=(2, 0, 1))

G.add_edge("P", "s1", cost=5)
G.add_edge("P", "s2", cost=10)
G.add_edge("s1", "s2", cost=3)

draw_graph.draw_graph(G, "Example 3D Graph")
