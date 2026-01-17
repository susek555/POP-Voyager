from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.ant_colony.common import AcoParams
from utils.config import Algorithm, AlgorithmType

DEFAULT_ANT_COUNT = 100
DEFAULT_ITERATIONS = 400
DEFAULT_ALPHA = 1.0
DEFAULT_BETA = 2.0
DEFAULT_DEGRADATION = 0.1
DEFAULT_Q = 300
DEFAULT_CANDIDATES_LIST_SIZE = 60
DEFAULT_DIFFUSION_RANGE = 1
DEFAULT_TIMES_TO_RUN = 10
DEFAULT_PATH_NODES = 10


def tune_aco_diffusion_range() -> list[Experiment]:
    experiment_name = "aco_diffused_tune_range"
    experiments = []
    for d_range in [1, 2, 3, 5]:
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
                    deposit_mode="diffusion",
                    diffusion_range=d_range,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_aco_diffusion_elite() -> list[Experiment]:
    experiment_name = "aco_diffused_tune_elite"
    experiments = []
    for elite in [1.0, 2.0, 5.0, 10.0]:
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
                    deposit_mode="diffusion",
                    diffusion_range=DEFAULT_DIFFUSION_RANGE,
                    elite_factor=elite,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def compare_standard_vs_diffusion() -> list[Experiment]:
    experiment_name = "aco_mode_comparison"
    experiments = []
    for mode in ["standard", "diffusion"]:
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
                    deposit_mode=mode,
                    diffusion_range=DEFAULT_DIFFUSION_RANGE if mode == "diffusion" else 0,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def get_all_aco_diffused_tuning_experiments() -> list[Experiment]:
    experiments = []
    experiments.extend(tune_aco_diffusion_range())
    experiments.extend(tune_aco_diffusion_elite())
    experiments.extend(compare_standard_vs_diffusion())
    return experiments


if __name__ == "__main__":
    all_diffused_tests = get_all_aco_diffused_tuning_experiments()

    ExperimentRunner.run_parallel(experiments=all_diffused_tests, max_workers=4, reuse_graph=True)
