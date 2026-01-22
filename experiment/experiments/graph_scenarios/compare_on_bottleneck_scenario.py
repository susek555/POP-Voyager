from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.bottleneck import BottleneckGraphParams  # Zakładana ścieżka
from utils.a_star import AStarParams, ChildrenFactory
from utils.ant_colony.common import AcoParams
from utils.config import Algorithm, AlgorithmParams, AlgorithmType
from utils.genetic import GeneticParams, ordered_crossover, select_tournament
from utils.sa import SAparams

PATH_NODES = 10
TIMES_TO_RUN = 30
EXP_NAME = "compare_on_bottleneck_scenario"

BOTTLENECK_SETUP = Graph(
    scenario=GraphScenario.BOTTLENECK,
    params=BottleneckGraphParams(
        nodes_per_side=20,
        bridge_nodes=1,
        side_distance=50.0,
        bubble_radius=15.0,
        reward_range=(20, 80),
        far_reward_multiplier=3.0,
        cost_factor=0.2
    ),
)


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

def random_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
        algorithm=Algorithm(
            type=AlgorithmType.RANDOM,
            params=AlgorithmParams(),
        ),
        nodes=PATH_NODES,
        times_to_run=TIMES_TO_RUN,
    )


def greedy_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
        algorithm=Algorithm(
            type=AlgorithmType.GREEDY,
            params=AlgorithmParams(),
        ),
        nodes=PATH_NODES,
        times_to_run=TIMES_TO_RUN,
    )


def sa_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
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
        nodes=PATH_NODES,
        times_to_run=TIMES_TO_RUN,
    )


def ga_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
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
        nodes=PATH_NODES,
        times_to_run=TIMES_TO_RUN,
    )


def aco_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
        algorithm=Algorithm(
            type=AlgorithmType.ACO,
            params=AcoParams(
                ant_count=DEFAULT_ANT_COUNT,
                iteration_count=DEFAULT_ITERATIONS,
                alpha=DEFAULT_ALPHA,
                beta=DEFAULT_BETA,
                pheromone_degradation_rate=DEFAULT_DEGRADATION,
                Q=DEFAULT_Q,
                candidate_list_size=DEFAULT_CANDIDATES_LIST_SIZE
            ),
        ),
        nodes=PATH_NODES,
        times_to_run=TIMES_TO_RUN,
    )

def a_star_compare_on_bottleneck_scenario() -> Experiment:
    return Experiment(
        name=EXP_NAME,
        graph=BOTTLENECK_SETUP,
        algorithm=Algorithm(
            type=AlgorithmType.A_STAR,
            params=AStarParams(
                childrenFactory=ChildrenFactory.N_BEST, n_children=DEFAULT_N_CHILDREN
            ),
        ),
        nodes=PATH_NODES,
        times_to_run=1,
    )


def get_all_compare_on_bottleneck_scenario() -> list[Experiment]:
    experiments = []
    experiments.append(random_compare_on_bottleneck_scenario())
    experiments.append(greedy_compare_on_bottleneck_scenario())
    experiments.append(sa_compare_on_bottleneck_scenario())
    experiments.append(ga_compare_on_bottleneck_scenario())
    experiments.append(aco_compare_on_bottleneck_scenario())
    experiments.append(a_star_compare_on_bottleneck_scenario())
    return experiments


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_bottleneck_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments,
        max_workers=4,
        reuse_graph=True
    )
