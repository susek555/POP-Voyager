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
    all_tuning_experiments = []
    all_tuning_experiments.extend(get_all_compare_on_base_graph())
    all_tuning_experiments.extend(get_all_compare_on_base_graph_25_nodes())
    all_tuning_experiments.extend(get_all_compare_on_base_graph_long_path())
    all_tuning_experiments.extend(get_all_compare_on_archipelago_scenario())
    all_tuning_experiments.extend(get_all_compare_on_line_circle_scenario())
    all_tuning_experiments.extend(get_all_compare_on_nebula_scenario())
    all_tuning_experiments.extend(get_all_compare_on_siren_song_scenario())
    all_tuning_experiments.extend(get_all_compare_on_gradient_scenario())
    all_tuning_experiments.extend(get_all_compare_on_bottleneck_scenario())

    ExperimentRunner.run_parallel(
        experiments=all_tuning_experiments, max_workers=4, reuse_graph=True
    )
