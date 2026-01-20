import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def analyze_tuning_results(file_path: str) -> None:
    data = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.json_normalize(data)

    param_cols = [c for c in df.columns if c.startswith("algorithm.params.")]

    varying_params = []
    for col in param_cols:
        if df[col].nunique() > 1:
            varying_params.append(col)

    if not varying_params:
        print(f"Did not detect varying parameters in file: {file_path}")
        return

    main_param = varying_params[0]
    param_display_name = main_param.split(".")[-1]

    df = df.sort_values(by=main_param)

    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    plt.errorbar(
        df[main_param].astype(str),
        df["result.average_score"],
        yerr=df["result.std_dev_score"],
        fmt="-o",
        capsize=5,
        linewidth=2,
        color="#2ecc71",
        ecolor="#e74c3c",
        label="Average Score (± Std Dev)",
    )

    experiment_name = df["experiment_name"].iloc[0]
    plt.title(
        f"Tuning Result: {experiment_name}\nImpact of {param_display_name} on Score", fontsize=14
    )
    plt.xlabel(f"Parameter: {param_display_name}", fontsize=12)
    plt.ylabel("Average Score (f_celu)", fontsize=12)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_img = file_path.replace("experiment/results/", "experiment/plots/tuning")
    output_img = file_path.replace(".jsonl", ".png")
    plt.savefig(output_img)
    print(f"Plot saved as: {output_img}")
    # plt.show()


if __name__ == "__main__":
    paths_to_results = [
        "experiment/results/aco_diffused.jsonl",
        "experiment/results/aco_diffused_tune_elite.jsonl",
        "experiment/results/aco_diffused_tune_range.jsonl",
        "experiment/results/aco_mode_comparison.jsonl",
        "experiment/results/aco_tune_alpha_beta.jsonl",
        "experiment/results/aco_tune_ant_count.jsonl",
        "experiment/results/aco_tune_candidates_list_size.jsonl",
        "experiment/results/aco_tune_degradation.jsonl",
        "experiment/results/aco_tune_evaporation.jsonl",
        "experiment/results/aco_tune_pheromone_influence.jsonl",
        "experiment/results/aco_tune_distance_influence.jsonl",
        "experiment/results/aco_tune_q_value.jsonl",
        "experiment/results/astar_tune_factory.jsonl",
        "experiment/results/astar_tune_n_children.jsonl",
        "experiment/results/ga_tune_generations.jsonl",
        "experiment/results/ga_tune_mutation_rate.jsonl",
        "experiment/results/ga_tune_pop_size.jsonl",
        "experiment/results/sa_tune_decrease_factor.jsonl",
        "experiment/results/sa_tune_n_iter.jsonl",
        "experiment/results/sa_tune_start_temp.jsonl",
    ]
    for path_to_results in paths_to_results:
        if os.path.exists(path_to_results):
            analyze_tuning_results(path_to_results)
        else:
            print("Results file not found.")
