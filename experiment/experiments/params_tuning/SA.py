from experiment.runner import Experiment
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.config import Algorithm, AlgorithmType
from utils.logger import setup_logger
from utils.sa import SAparams


def tune_n_iter() -> list[Experiment]:
    experiment_name = "sa_tune_n_iter"
    experiments = []
    for n_iter in [100, 200, 500, 1000, 2000, 5000, 10000, 20000]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.SA,
                params=SAparams(
                    n_iter=n_iter,
                    start_temp=100.0,
                    decrease_factor=0.99,
                    n_threads=4,
                    n_candidates_per_thread=4,
                ),
            ),
            max_nodes=10,
            times_to_run=10,
        )
        experiments.append(experiment)

    return experiments


def tune_sa_start_temp() -> list[Experiment]:
    experiment_name = "sa_tune_start_temp"
    experiments = []
    for start_temp in [10.0, 50.0, 100.0, 200.0, 500.0]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.SA,
                params=SAparams(
                    n_iter=5000,
                    start_temp=start_temp,
                    decrease_factor=0.99,
                    n_threads=4,
                    n_candidates_per_thread=4,
                ),
            ),
            max_nodes=10,
            times_to_run=10,
        )
        experiments.append(experiment)

    return experiments


def tune_sa_decrease_factor() -> list[Experiment]:
    experiment_name = "sa_tune_decrease_factor"
    experiments = []
    for decrease_factor in [0.90, 0.95, 0.99, 0.995, 0.999]:
        experiment = Experiment(
            name=f"{experiment_name}",
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.SA,
                params=SAparams(
                    n_iter=5000,
                    start_temp=100.0,
                    decrease_factor=decrease_factor,
                    n_threads=4,
                    n_candidates_per_thread=4,
                ),
            ),
            max_nodes=10,
            times_to_run=10,
        )
        experiments.append(experiment)

    return experiments


def get_all_sa_tuning_experiments() -> list[Experiment]:
    experiments = []
    experiments.extend(tune_n_iter())
    experiments.extend(tune_sa_start_temp())
    experiments.extend(tune_sa_decrease_factor())
    return experiments



if __name__ == "__main__":
    # import logging

    from experiment.runner import ExperimentRunner

    # setup_logger(logging.INFO)

    all_experiments = get_all_sa_tuning_experiments()
    ExperimentRunner.run_parallel(
        experiments=all_experiments,
        max_workers=4,
        reuse_graph=True,
    )
