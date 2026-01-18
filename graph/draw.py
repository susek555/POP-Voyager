import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import RadioButtons

from models.path import Path


def draw_graph(
    graph: nx.Graph,
    title: str,
    paths: dict[str, Path] | None = None,
    evals: dict[str, float] | None = None,
) -> None:
    if paths is None or not paths:
        paths = {"No Path": Path()}

    if evals is None:
        evals = {}
    radio_labels = []
    label_to_key = {}

    for key in paths:
        score = evals.get(key)
        display_label = f"{key}: {score:.2f}" if score is not None else key

        radio_labels.append(display_label)
        label_to_key[display_label] = key

    pos = nx.get_node_attributes(graph, "pos")
    fig = plt.figure(figsize=(12, 8))

    plt.subplots_adjust(left=0.25)
    ax = fig.add_subplot(111, projection="3d")

    for node, (x, y, z) in pos.items():
        reward = graph.nodes[node]["reward"]
        size = 100
        color = "green" if node == "P" else "orange"

        ax.scatter(x, y, z, s=size, label=node, color=color, edgecolors="black", alpha=0.8)

        offset = 0.05
        zmin, zmax = ax.get_zlim() if ax.get_zlim() else (-10, 10)
        scale = (zmax - zmin) * offset
        ax.text(x, y, z + scale, f"{node}", color="black", fontsize=9, ha="center", weight="bold")
        if reward > 0:
            ax.text(x, y, z - 3 * scale, f"{reward}", color="darkgreen", fontsize=8, ha="center")

    ax.set_facecolor("white")
    ax.grid(False)
    ax.set_axis_off()

    ax.set_title(title, fontsize=14)

    current_artists = []

    def draw_path(display_label: str) -> None:
        key = label_to_key[display_label]

        for artist in current_artists:
            artist.remove()
        current_artists.clear()

        score_text = f" | Score: {evals[key]:.4f}" if key in evals else ""
        ax.set_title(f"{title} - {key}{score_text}", fontsize=12)

        path = paths[key]
        if not path:
            fig.canvas.draw_idle()
            return

        for u, v in zip(path[:-1], path[1:], strict=False):
            if u not in pos or v not in pos:
                continue

            x = [pos[u][0], pos[v][0]]
            y = [pos[u][1], pos[v][1]]
            z = [pos[u][2], pos[v][2]]

            (line,) = ax.plot(x, y, z, color="blue", linewidth=2, alpha=0.7)
            current_artists.append(line)

            mid = [
                (pos[u][0] + pos[v][0]) / 2,
                (pos[u][1] + pos[v][1]) / 2,
                (pos[u][2] + pos[v][2]) / 2,
            ]

            cost_val = ""
            if graph.has_edge(u, v):
                cost_val = str(graph[u][v].get("cost", ""))

            text = ax.text(
                mid[0],
                mid[1],
                mid[2],
                cost_val,
                color="red",
                fontsize=9,
                fontweight="bold",
                zorder=10,
            )
            current_artists.append(text)

        fig.canvas.draw_idle()

    ax_color = "lightgoldenrodyellow"
    menu_height = 0.05 * len(radio_labels)
    rax = plt.axes([0.02, 0.5, 0.20, min(menu_height, 0.5)], facecolor=ax_color)

    radio = RadioButtons(rax, radio_labels)
    radio.on_clicked(draw_path)

    draw_path(radio_labels[0])

    plt.show()
