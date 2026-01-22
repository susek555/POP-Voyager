from experiment.experiments.compare_algs.compare_on_base_graph import get_all_compare_on_base_graph
from experiment.experiments.compare_algs.compare_on_base_graph_25_nodes import (
    get_all_compare_on_base_graph_25_nodes,
)
from experiment.experiments.compare_algs.compare_on_base_graph_long_path import (
    get_all_compare_on_base_graph_long_path,
)
from experiment.experiments.graph_scenarios.compare_on_archipelago_scenario import (
    get_all_compare_on_archipelago_scenario,
)
from experiment.experiments.graph_scenarios.compare_on_bottleneck_scenario import (
    get_all_compare_on_bottleneck_scenario,
)
from experiment.experiments.graph_scenarios.compare_on_gradient_scenario import (
    get_all_compare_on_gradient_scenario,
)
from experiment.experiments.graph_scenarios.compare_on_line_circle_scenario import (
    get_all_compare_on_line_circle_scenario,
)
from experiment.experiments.graph_scenarios.compare_on_nebula_scenario import (
    get_all_compare_on_nebula_scenario,
)
from experiment.experiments.graph_scenarios.compare_on_siren_song_scenario import (
    get_all_compare_on_siren_song_scenario,
)
from experiment.runner import ExperimentRunner

if __name__ == "__main__":
    groups = {
        "base_graph": get_all_compare_on_base_graph(),
        "base_graph_25_nodes": get_all_compare_on_base_graph_25_nodes(),
        "base_graph_long_path": get_all_compare_on_base_graph_long_path(),
        "archipelago_scenario": get_all_compare_on_archipelago_scenario(),
        "line_circle_scenario": get_all_compare_on_line_circle_scenario(),
        "nebula_scenario": get_all_compare_on_nebula_scenario(),
        "siren_song_scenario": get_all_compare_on_siren_song_scenario(),
        "gradient_scenario": get_all_compare_on_gradient_scenario(),
        "bottleneck_scenario": get_all_compare_on_bottleneck_scenario(),
    }

    for name, experiments in groups.items():
        print(f"--- Running group: {name} ---")
        ExperimentRunner.run_parallel(
            experiments=experiments,
            max_workers=4,
            reuse_graph=True,
        )
