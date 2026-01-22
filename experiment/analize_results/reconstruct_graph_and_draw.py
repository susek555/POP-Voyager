import json
import os

# Importy Twoich modułów
from graph.draw import draw_graph
from graph.generate import BasicGraphParams, generate_graph
from graph.scenarios.archipelago import ArchipelagoGraphParams, generate_archipelago_graph
from graph.scenarios.bottleneck import BottleneckGraphParams, generate_bottleneck_graph
from graph.scenarios.gradient import GradientGraphParams, generate_gradient_graph
from graph.scenarios.line_circle import LineCircleGraphParams, generate_line_circle_graph
from graph.scenarios.nebula import NebulaGraphParams, generate_nebula_graph
from graph.scenarios.siren_song import SirenSongGraphParams, generate_siren_song_graph
from heuristics.ant_colony import aco
from heuristics.genetic import genetic
from heuristics.greedy import greedy
from heuristics.random import full_random
from heuristics.sa import SA
from objective_function import objective_function
from utils.ant_colony.common import AcoParams
from utils.config import AlgorithmParams
from utils.genetic import GeneticParams, ordered_crossover, select_tournament
from utils.sa import SAparams


def reconstruct_and_draw(jsonl_path: str) -> None:
    experiments_data = []
    if not os.path.exists(jsonl_path):
        print(f"Błąd: Plik {jsonl_path} nie istnieje.")
        return

    with open(jsonl_path) as f:
        for line in f:
            experiments_data.append(json.loads(line))

    if not experiments_data:
        print("Plik jest pusty.")
        return

    base_info = experiments_data[0]
    g_params_raw = base_info["graph"]["params"]
    scenario_name = base_info["graph"]["scenario"]

    print(f"--- Rekonstrukcja grafu: {scenario_name} (seed: {g_params_raw['seed']}) ---")

    generators = {
        "BASIC": (generate_graph, BasicGraphParams),
        "ARCHIPELAGO": (generate_archipelago_graph, ArchipelagoGraphParams),
        "BOTTLENECK": (generate_bottleneck_graph, BottleneckGraphParams),
        "GRADIENT": (generate_gradient_graph, GradientGraphParams),
        "LINE_CIRCLE": (generate_line_circle_graph, LineCircleGraphParams),
        "NEBULA": (generate_nebula_graph, NebulaGraphParams),
        "SIREN_SONG": (generate_siren_song_graph, SirenSongGraphParams),
    }

    gen_func, param_class = generators[scenario_name]
    g_params = param_class(**{k: v for k, v in g_params_raw.items() if k != "seed"})
    g_params.seed = g_params_raw["seed"]
    G = gen_func(g_params)

    paths = {}
    evals = {}
    max_nodes = base_info["max_nodes"]

    for exp in experiments_data:
        algo_type = exp["algorithm"]["type"]
        algo_params_raw = exp["algorithm"]["params"]
        seed = exp.get("base_seed", 42)

        try:
            if algo_type == "A_STAR":
                print(f"Odczytywanie zapisanego wyniku dla: {algo_type} (pomijanie obliczeń)...")
                path = exp["result"]["best_path"]
                score = exp["result"]["best_score"]

            else:
                print(f"Uruchamianie algorytmu: {algo_type}...")

                if algo_type == "RANDOM":
                    p = AlgorithmParams(seed=seed)
                    path = full_random(G, max_nodes, p)

                elif algo_type == "GREEDY":
                    path = greedy(G, max_nodes)

                elif algo_type == "SA":
                    p = SAparams(**{k: v for k, v in algo_params_raw.items() if k != "seed"})
                    p.seed = seed
                    path = SA(G, objective_function, max_nodes, p)

                elif algo_type == "GENETIC":
                    p = GeneticParams(
                        pop_size=algo_params_raw["pop_size"],
                        generations=algo_params_raw["generations"],
                        mutation_rate=algo_params_raw["mutation_rate"],
                        crossover=ordered_crossover,
                        selection=select_tournament,
                        selection_kwargs=algo_params_raw["selection_kwargs"],
                    )
                    path = genetic(G, objective_function, max_nodes, p)

                elif algo_type == "ACO":
                    p = AcoParams(**{k: v for k, v in algo_params_raw.items() if k != "seed"})
                    p.seed = seed
                    path = aco(G, objective_function, max_nodes, p)

                else:
                    print(f"Pominięto nieznany typ: {algo_type}")
                    continue

                score = objective_function(G, path)

            label = f"{algo_type} (score: {score:.2f})"
            paths[label] = path
            evals[label] = score

        except Exception as e:
            print(f"Błąd podczas przetwarzania {algo_type}: {e}")

    print("Otwieranie okna wizualizacji...")
    draw_graph(G, f"Wizualizacja: {scenario_name}", paths, evals)


if __name__ == "__main__":
    reconstruct_and_draw("experiment/results/compare_on_line_circle_scenario.jsonl")
