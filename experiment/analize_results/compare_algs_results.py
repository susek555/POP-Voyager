import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_scenario_results(filepath: str, title: str) -> None:
    with open(filepath) as file:
        data = [json.loads(line) for line in file]
    df = pd.json_normalize(data)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    sns.barplot(
        data=df,
        x="algorithm.type",
        y="result.average_score",
        ax=ax1,
        palette="viridis",
        capsize=0.1,
    )

    for container in ax1.containers:
        ax1.bar_label(container, fmt="%.2f", padding=3, fontweight="bold")

    ax1.set_ylabel("Średni Wynik (f_celu)", fontsize=12, color="#27ae60")
    ax1.set_xlabel("Algorytm", fontsize=12)

    ax2 = ax1.twinx()
    ax2.plot(
        df["algorithm.type"],
        df["result.average_time"],
        color="#e74c3c",
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Czas (s)",
    )
    ax2.set_ylabel("Czas wykonania (s)", fontsize=12, color="#e74c3c")
    ax2.grid(False)

    plt.title(f"Porównanie algorytmów: {title}", fontsize=15)
    plt.tight_layout()
    plt.savefig(filepath.replace(".jsonl", ".png"))


def plot_metaheuristic_vs_astar(filepath: str, title: str) -> None:
    with open(filepath) as file:
        data = [json.loads(line) for line in file]

    full_df = pd.json_normalize(data)

    astar_data = full_df[full_df["algorithm.type"] == "A_STAR"]
    astar_score = astar_data["result.average_score"].iloc[0] if not astar_data.empty else None

    df = full_df[full_df["algorithm.type"] != "A_STAR"].copy()

    if df.empty:
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 11), sharex=True)
    sns.set_theme(style="whitegrid")

    sns.barplot(data=df, x="algorithm.type", y="result.average_score", ax=ax1, palette="viridis")

    for container in ax1.containers:
        ax1.bar_label(container, fmt="%.2f", padding=3, fontweight="bold")

    if astar_score is not None:
        ax1.axhline(
            y=astar_score,
            color="r",
            linestyle="--",
            linewidth=2,
            label=f"Baseline (A*): {astar_score:.2f}",
        )
        ax1.legend(loc="lower right", frameon=True, shadow=True)

    ax1.set_title(f"Porównanie algorytmów: {title}", fontsize=16, pad=20)
    ax1.set_ylabel("Średni Wynik (f_celu)", fontsize=12)

    sns.barplot(data=df, x="algorithm.type", y="result.average_time", ax=ax2, palette="flare")

    for container in ax2.containers:
        ax2.bar_label(container, fmt="%.2f s", padding=3)

    ax2.set_ylabel("Średni Czas Wykonania (s)", fontsize=12)
    ax2.set_xlabel("Algorytm", fontsize=12)

    if not astar_data.empty:
        astar_time = astar_data["result.average_time"].iloc[0]
        plt.figtext(
            0.98,
            0.01,
            f"Info: Czas A* = {astar_time:.2f} s",
            horizontalalignment="right",
            fontsize=10,
            color="red",
            style="italic",
        )

    plt.tight_layout()
    output_name = filepath.replace(".jsonl", "_full_comparison.png")
    plt.savefig(output_name, dpi=300)
    plt.close()


if __name__ == "__main__":
    # plot_scenario_results(
    #     "experiment/results/compare_on_base_graph_25_nodes.jsonl",
    #     "Podstawowy Graf - 25 Węzłów",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_base_graph_long_path.jsonl",
    #     "Podstawowy Graf - Długa Ścieżka",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_base_graph.jsonl",
    #     "Podstawowy Graf",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_archipelago_scenario.jsonl",
    #     "Scenariusz Archipelagu",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_line_circle_scenario.jsonl",
    #     "Scenariusz Linia i Koło",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_nebula_scenario.jsonl",
    #     "Scenariusz Mgławicy",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_siren_song_scenario.jsonl",
    #     "Scenariusz Pieśni Syreny",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_gradient_scenario.jsonl",
    #     "Scenariusz Gradientu",
    # )
    # plot_scenario_results(
    #     "experiment/results/compare_on_bottleneck_scenario.jsonl",
    #     "Scenariusz Wąskiego Gardła",
    # )
    plot_scenario_results(
        "experiment/results/compare_on_barabasi_20_nodes_extended_path.jsonl",
        "Graf typu Barabási - (20 węzłów, ścieżka 10)",
    )
    plot_scenario_results(
        "experiment/results/compare_on_barabasi_40_nodes_extended_path.jsonl",
        "Graf typu Barabási - (40 węzłów, ścieżka 20)",
    )
    plot_scenario_results(
        "experiment/results/compare_on_barabasi_60_nodes_extended_path.jsonl",
        "Graf typu Barabási - (60 węzłów, ścieżka 30)",
    )
    plot_scenario_results(
        "experiment/results/compare_on_barabasi_80_nodes_extended_path.jsonl",
        "Graf typu Barabási - (80 węzłów, ścieżka 40)",
    )
    plot_scenario_results(
        "experiment/results/compare_on_barabasi_100_nodes_extended_path.jsonl",
        "Graf typu Barabási - (100 węzłów, ścieżka 50)",
    )
