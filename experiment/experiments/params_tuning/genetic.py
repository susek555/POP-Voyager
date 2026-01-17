from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.config import Algorithm, AlgorithmType
from utils.genetic import GeneticParams, ordered_crossover, select_tournament

DEFAULT_POP_SIZE = 50
DEFAULT_GENERATIONS = 200
DEFAULT_MUTATION_RATE = 0.15
DEFAULT_TOURNAMENT_SIZE = 3
DEFAULT_TIMES_TO_RUN = 10
DEFAULT_PATH_NODES = 10


def tune_ga_pop_size() -> list[Experiment]:
    experiment_name = "ga_tune_pop_size"
    experiments = []
    for pop_size in [10, 20, 50, 100, 200, 500]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.GENETIC,
                params=GeneticParams(
                    pop_size=pop_size,
                    generations=DEFAULT_GENERATIONS,
                    mutation_rate=DEFAULT_MUTATION_RATE,
                    crossover=ordered_crossover,
                    selection=select_tournament,
                    selection_kwargs={"tournament_size": DEFAULT_TOURNAMENT_SIZE},
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_ga_generations() -> list[Experiment]:
    experiment_name = "ga_tune_generations"
    experiments = []
    for generations in [50, 100, 200, 500, 1000, 2000]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.GENETIC,
                params=GeneticParams(
                    pop_size=DEFAULT_POP_SIZE,
                    generations=generations,
                    mutation_rate=DEFAULT_MUTATION_RATE,
                    crossover=ordered_crossover,
                    selection=select_tournament,
                    selection_kwargs={"tournament_size": DEFAULT_TOURNAMENT_SIZE},
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_ga_mutation_rate() -> list[Experiment]:
    experiment_name = "ga_tune_mutation_rate"
    experiments = []
    for mutation_rate in [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.GENETIC,
                params=GeneticParams(
                    pop_size=DEFAULT_POP_SIZE,
                    generations=DEFAULT_GENERATIONS,
                    mutation_rate=mutation_rate,
                    crossover=ordered_crossover,
                    selection=select_tournament,
                    selection_kwargs={"tournament_size": DEFAULT_TOURNAMENT_SIZE},
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def get_all_ga_tuning_experiments() -> list[Experiment]:
    experiments = []
    experiments.extend(tune_ga_pop_size())
    experiments.extend(tune_ga_generations())
    experiments.extend(tune_ga_mutation_rate())
    return experiments


if __name__ == "__main__":
    all_ga_experiments = get_all_ga_tuning_experiments()

    ExperimentRunner.run_parallel(
        experiments=all_ga_experiments,
        max_workers=4,
        reuse_graph=True,
    )
