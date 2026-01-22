from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from graph.scenarios.siren_song import SirenSongGraphParams

PATH_NODES = 10
EXP_NAME = "compare_on_siren_song_scenario"

SIREN_SONG_SETUP = Graph(
    scenario=GraphScenario.SIREN_SONG,
    params=SirenSongGraphParams(
        n_local_nodes=30,
        local_dist_range=(5.0, 20.0),
        local_reward_range=(5, 15),
        siren_distance=150.0,
        siren_reward=800,
        cost_factor=0.2,
    ),
)


def get_all_compare_on_siren_song_scenario() -> list[Experiment]:
    return get_compare_on_scenarios_experiment(PATH_NODES, EXP_NAME, SIREN_SONG_SETUP)


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_siren_song_scenario()

    ExperimentRunner.run_parallel(
        experiments=all_compare_experiments, max_workers=4, reuse_graph=True
    )
