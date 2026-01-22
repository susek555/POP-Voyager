from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.ant_colony.common import AcoParams
from utils.config import Algorithm, AlgorithmType

DEFAULT_ANT_COUNT = 50
DEFAULT_ITERATIONS = 800
DEFAULT_ALPHA = 1.0
DEFAULT_BETA = 1.0
DEFAULT_DEGRADATION = 0.3
DEFAULT_Q = 50
DEFAULT_CANDIDATES_LIST_SIZE = 10
DEFAULT_TIMES_TO_RUN = 10
DEFAULT_PATH_NODES = 10


def tune_aco_ant_count() -> list[Experiment]:
    experiment_name = "aco_tune_ant_count"
    experiments = []
    for ant_count in [5, 10, 20, 50, 100, 200]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=ant_count,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_alpha() -> list[Experiment]:
    experiment_name = "aco_tune_alpha"
    experiments = []
    for alpha in [0.01, 0.5, 1.0, 2.0, 5.0, 10.0]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=alpha,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_beta() -> list[Experiment]:
    experiment_name = "aco_tune_beta"
    experiments = []
    for beta in [0.01, 0.5, 1.0, 2.0, 5.0, 10.0]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=beta,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_degradation() -> list[Experiment]:
    experiment_name = "aco_tune_degradation"
    experiments = []
    for rate in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=rate,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_candidates_list_size() -> list[Experiment]:
    experiment_name = "aco_tune_candidates_list_size"
    experiments = []
    for cls in [0, 5, 10, 20, 50]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=cls,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_q_value() -> list[Experiment]:
    experiment_name = "aco_tune_q_value"
    experiments = []
    for q in [10, 50, 100, 200, 300, 500]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_iterations() -> list[Experiment]:
    experiment_name = "aco_tune_iterations"
    experiments = []
    for iterations in [50, 100, 200, 400, 800, 1600]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=iterations,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_elite() -> list[Experiment]:
    experiment_name = "aco_tune_elite"
    experiments = []
    for elite in [0.0, 1.0, 2.0, 5.0, 10.0]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(scenario=GraphScenario.BASIC, params=BasicGraphParams()),
            algorithm=Algorithm(
                type=AlgorithmType.ACO,
                params=AcoParams(
                    ant_count=DEFAULT_ANT_COUNT,
                    iteration_count=DEFAULT_ITERATIONS,
                    alpha=DEFAULT_ALPHA,
                    beta=DEFAULT_BETA,
                    pheromone_degradation_rate=DEFAULT_DEGRADATION,
                    Q=DEFAULT_Q,
                    candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE,
                    elite_factor=elite,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def get_all_aco_tuning_experiments() -> list[Experiment]:
    experiments = []
    experiments.extend(tune_aco_ant_count())
    experiments.extend(tune_aco_alpha())
    experiments.extend(tune_aco_beta())
    experiments.extend(tune_aco_degradation())
    experiments.extend(tune_aco_candidates_list_size())
    experiments.extend(tune_aco_q_value())
    experiments.extend(tune_aco_elite())
    return experiments


if __name__ == "__main__":
    all_aco_experiments = get_all_aco_tuning_experiments()

    ExperimentRunner.run_parallel(experiments=all_aco_experiments, max_workers=4, reuse_graph=True)
