from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.nebula import NebulaGraphParams

PATH_NODES = 10
EXP_NAME = "compare_on_nebula_scenario"

NEBULA_SETUP = Graph(
    scenario=GraphScenario.NEBULA,
    params=NebulaGraphParams(
        n_nodes=50,
        cloud_radius=70.0,
        nebula_center=(30.0, 0.0, 0.0),
        nebula_radius=20.0,
        nebula_multiplier=4.0,
        reward_range=(15, 60),
        cost_factor=0.2,
    ),
)


def get_all_compare_on_nebula_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, NEBULA_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_nebula_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
