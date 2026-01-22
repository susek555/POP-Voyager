from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.bottleneck import BottleneckGraphParams

PATH_NODES = 10
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
        cost_factor=0.2,
    ),
)


def get_all_compare_on_bottleneck_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, BOTTLENECK_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_bottleneck_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
