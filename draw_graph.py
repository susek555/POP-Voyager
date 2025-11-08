import matplotlib.pyplot as plt
import networkx as nx

from models.path import Path


def draw_graph(graph: nx.Graph, title: str, path: Path | None = None) -> None:
    if path is None:
        path = Path()

    # Get 3D positions
    pos = nx.get_node_attributes(graph, "pos")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # All Edges
    # for (u, v, d) in graph.edges(data=True):
    #     x = [pos[u][0], pos[v][0]]
    #     y = [pos[u][1], pos[v][1]]
    #     z = [pos[u][2], pos[v][2]]
    #     ax.plot(x, y, z, color='gray')
    #     mid = [(pos[u][0]+pos[v][0])/2, (pos[u][1]+pos[v][1])/2, (pos[u][2]+pos[v][2])/2]
    #     ax.text(mid[0], mid[1], mid[2], f"{d['cost']}", color='red', fontsize=8)

    # Edges in path
    for u, v in zip(path[:-1], path[1:], strict=False):
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        z = [pos[u][2], pos[v][2]]
        ax.plot(x, y, z, color="blue")
        mid = [
            (pos[u][0] + pos[v][0]) / 2,
            (pos[u][1] + pos[v][1]) / 2,
            (pos[u][2] + pos[v][2]) / 2,
        ]
        ax.text(mid[0], mid[1], mid[2], f"{graph[u][v]['cost']}", color="red", fontsize=8)

    # Nodes
    for node, (x, y, z) in pos.items():
        reward = graph.nodes[node]["reward"]
        size = 100

        ax.scatter(x, y, z, s=size, label=node, color=("green" if node == "P" else "orange"))

        offset = 0.05  # procent osi Z

        zmin, zmax = ax.get_zlim()
        scale = (zmax - zmin) * offset

        ax.text(x, y, z + scale, f"{node}", color="green", fontsize=9, ha="center")
        ax.text(x, y, z - 3 * scale, f"{reward}", color="green", fontsize=9, ha="center")

    # Clear background
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_axis_off()

    ax.set_title(title)
    plt.show()
