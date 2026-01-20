import json
import os

import pandas as pd


def extract_best_configs(filepaths: list[str] = None) -> None:
    all_results = []

    for file_path in filepaths:
        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        all_results.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

    if not all_results:
        print("No results to analyze.")
        return

    df = pd.json_normalize(all_results)

    df_sorted = df.sort_values(
        by=["result.average_score", "result.std_dev_score", "result.average_time"],
        ascending=[False, True, True],
    )

    best_per_algo = df_sorted.drop_duplicates(subset=["algorithm.type"])

    print("-" * 50)
    print("BEST PARAMETER SETS FOR EACH ALGORITHM")
    print("-" * 50)

    for _, row in best_per_algo.iterrows():
        algo_type = row["algorithm.type"]
        print(f"\nAlgorithm: {algo_type}")
        print(f"Average Score: {row['result.average_score']}")
        print(f"Standard Deviation: {row['result.std_dev_score']}")
        print(f"Average Time: {row['result.average_time']}s")

        params = {
            k.replace("algorithm.params.", ""): v
            for k, v in row.items()
            if k.startswith("algorithm.params.") and pd.notna(v)
        }

        print(f"Parameters: {json.dumps(params, indent=4, ensure_ascii=False)}")
        print("-" * 30)


if __name__ == "__main__":
    extract_best_configs(
        filepaths=[
            "experiment/results/aco_random_search_tuning.jsonl",
            "experiment/results/sa_random_search_tuning.jsonl",
            "experiment/results/genetic_random_search_tuning.jsonl",
        ]
    )
