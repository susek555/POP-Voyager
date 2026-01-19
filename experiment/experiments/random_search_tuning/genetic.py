import random

from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.config import Algorithm, AlgorithmType
from utils.genetic import GeneticParams, ordered_crossover, select_tournament


def random_search_genetic(n_samples: int = 300) -> list[Experiment]:
    experiments = []

    space = {
        "pop_sizes": [20, 50, 100, 200, 500],
        "generations": [50, 100, 200, 500, 1000],
        "mutation_rates": [0.01, 0.05, 0.1, 0.15, 0.2, 0.3],
        "tournament_sizes": [2, 3, 5, 7],
        "no_improvement_stops": [None, 25, 50, 100, 200],
    }

    for _ in range(n_samples):
        exp = Experiment(
            name="genetic_hypergrid_search",
            nodes=10,
            times_to_run=5,
            seed=42,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.GENETIC,
                params=GeneticParams(
                    pop_size=random.choice(space["pop_sizes"]),
                    generations=random.choice(space["generations"]),
                    mutation_rate=random.choice(space["mutation_rates"]),
                    crossover=ordered_crossover,
                    selection=select_tournament,
                    selection_kwargs={"tournament_size": random.choice(space["tournament_sizes"])},
                    no_improvement_stop=random.choice(space["no_improvement_stops"]),
                ),
            ),
        )
        experiments.append(exp)

    return experiments


if __name__ == "__main__":
    all_tuning_experiments = []
    all_tuning_experiments.extend(random_search_genetic(n_samples=300))

    ExperimentRunner.run_parallel(
        experiments=all_tuning_experiments, max_workers=4, reuse_graph=True
    )
