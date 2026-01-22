from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.a_star import AStarParams, ChildrenFactory
from utils.config import Algorithm, AlgorithmType

DEFAULT_N_CHILDREN = 10
DEFAULT_TIMES_TO_RUN = 1
DEFAULT_PATH_NODES = 10


def tune_astar_n_children() -> list[Experiment]:
    experiment_name = "astar_tune_n_children"
    experiments = []
    for n in [1, 3, 5, 10, 15]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(number_of_nodes=20, cost_factor=0.2),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.A_STAR,
                params=AStarParams(childrenFactory=ChildrenFactory.N_BEST, n_children=n),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def tune_astar_factory() -> list[Experiment]:
    experiment_name = "astar_tune_factory"
    experiments = []
    for factory in [ChildrenFactory.ALL, ChildrenFactory.N_BEST]:
        experiment = Experiment(
            name=experiment_name,
            graph=Graph(
                scenario=GraphScenario.BASIC,
                params=BasicGraphParams(number_of_nodes=20, cost_factor=0.2),
            ),
            algorithm=Algorithm(
                type=AlgorithmType.A_STAR,
                params=AStarParams(
                    childrenFactory=factory,
                    n_children=DEFAULT_N_CHILDREN if factory == ChildrenFactory.N_BEST else 0,
                ),
            ),
            nodes=DEFAULT_PATH_NODES,
            times_to_run=DEFAULT_TIMES_TO_RUN,
        )
        experiments.append(experiment)
    return experiments


def get_all_astar_tuning_experiments() -> list[Experiment]:
    experiments = []
    experiments.extend(tune_astar_n_children())
    experiments.extend(tune_astar_factory())
    return experiments


if __name__ == "__main__":
    all_astar_tests = get_all_astar_tuning_experiments()

    ExperimentRunner.run_parallel(experiments=all_astar_tests, max_workers=4, reuse_graph=True)
