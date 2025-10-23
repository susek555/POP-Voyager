import networkx as nx

G = nx.Graph()


G.add_node("P")
G.add_node("s1")
G.add_node("s2")

G.add_edge("P", "s1")
G.add_edge("P", "s2")
G.add_edge("s1", "s2")

G["P"]["s1"]["cost"] = 5
G["P"]["s2"]["cost"] = 10
G["s1"]["s2"]["cost"] = 3

G.nodes["s1"]["reward"] = 15
G.nodes["s2"]["reward"] = 20
G.nodes["P"]["reward"] = 0

print(G.nodes(data=True))
print(G.edges(data=True))
