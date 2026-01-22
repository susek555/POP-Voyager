import json
from pathlib import Path

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
    varying_params = [col for col in param_cols if df[col].nunique() > 1]

    if not varying_params:
        return

    main_param = varying_params[0]
    param_display_name = main_param.split(".")[-1]
    df = df.sort_values(by=main_param)

    fig, ax1 = plt.subplots(figsize=(12, 7))
    sns.set_theme(style="whitegrid")

    ax1.errorbar(
        df[main_param].astype(str),
        df["result.average_score"],
        yerr=df.get("result.std_dev_score", 0),
        fmt="-o",
        capsize=6,
        linewidth=2.5,
        color="#27ae60",
        ecolor="#2ecc71",
        label="Średni wynik (± Std Dev)",
    )

    ax1.set_xlabel(f"Parametr: {param_display_name}", fontsize=12)
    ax1.set_ylabel("Wynik (f_celu)", fontsize=12, color="#27ae60")
    ax1.tick_params(axis="y", labelcolor="#27ae60")

    time_col = next(
        (
            c
            for c in ["result.average_time", "result.time", "result.execution_time"]
            if c in df.columns
        ),
        None,
    )

    if time_col:
        ax2 = ax1.twinx()
        ax2.plot(
            df[main_param].astype(str),
            df[time_col],
            color="#e74c3c",
            linestyle="--",
            marker="s",
            markersize=8,
            alpha=0.8,
            label="Czas wykonania (s)",
        )
        ax2.set_ylabel("Czas (sekundy)", fontsize=12, color="#e74c3c")
        ax2.tick_params(axis="y", labelcolor="#e74c3c")
        ax2.grid(False)

    plt.title(
        f"Analiza parametru: {param_display_name}\nWyniki vs Czas wykonania",
        fontsize=14,
        pad=20,
    )

    lines1, labels1 = ax1.get_legend_handles_labels()
    if time_col:
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, shadow=True)
    else:
        ax1.legend(loc="upper left", frameon=True, shadow=True)

    plt.xticks(rotation=45)
    plt.tight_layout()

    output_img = file_path.replace(".jsonl", "_detailed.png")
    plt.savefig(output_img, dpi=300)
    plt.close()
    print(f"Wygenerowano wykres: {output_img}")


if __name__ == "__main__":
    results_dir = Path("experiment/results")
    results = [str(file) for file in results_dir.iterdir() if file.suffix == ".jsonl"]

    for path in results:
        analyze_tuning_results(path)
