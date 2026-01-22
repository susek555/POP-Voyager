from experiment.experiments.params_tuning.a_star import get_all_astar_tuning_experiments
from experiment.experiments.params_tuning.aco import get_all_aco_tuning_experiments
from experiment.experiments.params_tuning.aco_diffused import (
    get_all_aco_diffused_tuning_experiments,
)
from experiment.experiments.params_tuning.genetic import get_all_ga_tuning_experiments
from experiment.experiments.params_tuning.sa import get_all_sa_tuning_experiments
from experiment.runner import ExperimentRunner

if __name__ == "__main__":
    all_tuning_experiments = []
    all_tuning_experiments.extend(get_all_sa_tuning_experiments())
    all_tuning_experiments.extend(get_all_ga_tuning_experiments())
    all_tuning_experiments.extend(get_all_aco_tuning_experiments())
    all_tuning_experiments.extend(get_all_aco_diffused_tuning_experiments())
    all_tuning_experiments.extend(get_all_astar_tuning_experiments())

    ExperimentRunner.run_parallel(
        experiments=all_tuning_experiments, max_workers=4, reuse_graph=True
    )
