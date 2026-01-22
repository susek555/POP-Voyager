from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.gradient import GradientGraphParams

PATH_NODES = 10
EXP_NAME = "compare_on_gradient_scenario"

GRADIENT_SETUP = Graph(
    scenario=GraphScenario.GRADIENT,
    params=GradientGraphParams(
        n_nodes=50, max_dist=100.0, base_reward=15, reward_scaling=8.0, cost_factor=0.2
    ),
)


def get_all_compare_on_gradient_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, GRADIENT_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_gradient_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
