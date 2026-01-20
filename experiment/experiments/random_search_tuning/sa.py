import random

from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.config import Algorithm, AlgorithmType
from utils.sa import SAparams


def random_search_sa(n_samples: int = 300) -> list[Experiment]:
    experiments = []

    space = {
        "n_iters": [200, 500, 1000, 2000, 5000],
        "start_temps": [10.0, 25.0, 50.0, 100.0],
        "decrease_factors": [0.8, 0.9, 0.995, 0.99, 0.98, 0.95],
    }

    for _ in range(n_samples):
        exp = Experiment(
            name="sa_random_search_tuning",
            nodes=10,
            times_to_run=5,
            seed=42,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.SA,
                params=SAparams(
                    n_iter=random.choice(space["n_iters"]),
                    start_temp=random.choice(space["start_temps"]),
                    decrease_factor=random.choice(space["decrease_factors"]),
                    n_threads=4,
                    n_candidates_per_thread=4,
                ),
            ),
        )
        experiments.append(exp)

    return experiments


if __name__ == "__main__":
    all_tuning_experiments = []
    all_tuning_experiments.extend(random_search_sa(n_samples=300))

    ExperimentRunner.run_parallel(
        experiments=all_tuning_experiments, max_workers=4, reuse_graph=True
    )
