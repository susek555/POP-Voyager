from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.generate import BasicGraphParams
from utils.a_star import AStarParams, ChildrenFactory
from utils.ant_colony.common import AcoParams
from utils.config import Algorithm, AlgorithmParams, AlgorithmType
from utils.genetic import GeneticParams, ordered_crossover, select_tournament
from utils.sa import SAparams

DEFAULT_TIMES_TO_RUN = 30
DEFAULT_PATH_NODES = 10

# SA
DEFAULT_N_ITER = 5000
DEFAULT_START_TEMP = 10
DEFAULT_DECREASE_FACTOR = 0.995

# GENETIC
DEFAULT_POP_SIZE = 500
DEFAULT_GENERATIONS = 500
DEFAULT_MUTATION_RATE = 0.1
DEFAULT_TOURNAMENT_SIZE = 2

# ACO
DEFAULT_ANT_COUNT = 50
DEFAULT_ITERATIONS = 800
DEFAULT_ALPHA = 1.0
DEFAULT_BETA = 1.0
DEFAULT_DEGRADATION = 0.3
DEFAULT_Q = 50
DEFAULT_CANDIDATES_LIST_SIZE = 10

# A_STAR
DEFAULT_N_CHILDREN = 10


def random_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.RANDOM,
            params=AlgorithmParams(),
        ),
        nodes=DEFAULT_PATH_NODES,
        times_to_run=DEFAULT_TIMES_TO_RUN,
    )

    return experiment


def greedy_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.GREEDY,
            params=AlgorithmParams(),
        ),
        nodes=DEFAULT_PATH_NODES,
        times_to_run=1,
    )

    return experiment


def sa_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.SA,
            params=SAparams(
                n_iter=DEFAULT_N_ITER,
                start_temp=DEFAULT_START_TEMP,
                decrease_factor=DEFAULT_DECREASE_FACTOR,
                n_threads=4,
                n_candidates_per_thread=4,
            ),
        ),
        nodes=DEFAULT_PATH_NODES,
        times_to_run=DEFAULT_TIMES_TO_RUN,
    )

    return experiment


def ga_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.GENETIC,
            params=GeneticParams(
                pop_size=DEFAULT_POP_SIZE,
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

    return experiment


def aco_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
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
            ),
        ),
        nodes=DEFAULT_PATH_NODES,
        times_to_run=DEFAULT_TIMES_TO_RUN,
    )

    return experiment


def a_start_compare_on_base_graph_25_nodes() -> Experiment:
    experiment_name = "compare_on_base_graph_25_nodes"
    experiment = Experiment(
        name=f"{experiment_name}",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(number_of_nodes=25),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.A_STAR,
            params=AStarParams(
                childrenFactory=ChildrenFactory.N_BEST, n_children=DEFAULT_N_CHILDREN
            ),
        ),
        nodes=DEFAULT_PATH_NODES,
        times_to_run=1,
    )

    return experiment


def get_all_compare_on_base_graph_25_nodes() -> list[Experiment]:
    experiments = []
    experiments.append(random_compare_on_base_graph_25_nodes())
    experiments.append(greedy_compare_on_base_graph_25_nodes())
    experiments.append(sa_compare_on_base_graph_25_nodes())
    experiments.append(ga_compare_on_base_graph_25_nodes())
    experiments.append(aco_compare_on_base_graph_25_nodes())
    experiments.append(a_start_compare_on_base_graph_25_nodes())
    return experiments


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_base_graph_25_nodes()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
