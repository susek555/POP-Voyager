import random

from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.ant_colony.common import AcoParams
from utils.config import Algorithm, AlgorithmType


def random_search_aco(n_samples: int = 300) -> list[Experiment]:
    experiments = []

    space = {
        'alpha_values': [0.5, 1.0, 2.0],
        'beta_values': [1.0, 2.0, 5.0],
        'degradation_rates': [0.05, 0.1, 0.3, 0.5, 0.7, 0.9],
        'candidate_list_sizes': [10, 30, 60, 100, 150],
        'iteration_counts': [100, 200, 400, 800, 1600],
        'q_values': [50, 100, 200, 300, 500],
        'ant_counts': [5, 10, 20, 50, 100]
    }

    for _ in range(n_samples):
        exp = Experiment(
            name="aco_hypergrid_search",
            nodes=10,
            times_to_run=5,
            seed=42,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    alpha=random.choice(space['alpha_values']),
                    beta=random.choice(space['beta_values']),
                    pheromone_degradation_rate=random.choice(space['degradation_rates']),
                    ant_count=random.choice(space['ant_counts']),
                    iteration_count=random.choice(space['iteration_counts']),
                    Q=random.choice(space['q_values']),
                    candidate_list_size=random.choice(space['candidate_list_sizes'])
                ),
            ),
        )
        experiments.append(exp)

    return experiments


if __name__ == "__main__":
    all_tuning_experiments = []
    all_tuning_experiments.extend(random_search_aco(n_samples=300))

    ExperimentRunner.run_parallel(
        experiments=all_tuning_experiments, max_workers=4, reuse_graph=True
    )
