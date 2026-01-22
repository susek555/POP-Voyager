from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.line_circle import LineCircleGraphParams

PATH_NODES = 10
EXP_NAME = "compare_on_line_circle_scenario"

LINE_CIRCLE_SETUP = Graph(
    scenario=GraphScenario.LINE_CIRCLE,
    params=LineCircleGraphParams(
        n_nodes_line=10,
        n_nodes_circle=20,
        line_dist=1.0,
        circle_radius=500.0,
        reward_range=(10, 100),
        cost_factor=0.6,
        circle_multiplier=100.0,
    ),
)


def get_all_compare_on_line_circle_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, LINE_CIRCLE_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_line_circle_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
