from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.archipelago import ArchipelagoGraphParams

PATH_NODES = 10
EXP_NAME = "compare_on_archipelago_scenario"

ARCHIPELAGO_SETUP = Graph(
    scenario=GraphScenario.ARCHIPELAGO,
    params=ArchipelagoGraphParams(
        n_clusters=4,
        nodes_per_cluster=8,
        cluster_spread=10.0,
        map_size=100.0,
        reward_range=(20, 1000),
        cost_factor=0.2,
    ),
)


def get_all_compare_on_archipelago_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, ARCHIPELAGO_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_archipelago_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
