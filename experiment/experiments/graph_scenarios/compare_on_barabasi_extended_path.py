import multiprocessing

from experiment.experiments.graph_scenarios.get_compare_on_scenarios_experiment import (
    get_compare_on_scenarios_experiment,
)
from experiment.runner import Experiment, ExperimentRunner
from graph.barabasi import BarabasiRadialParams
from graph.config import Graph, GraphScenario

PATH_NODES = 20


def get_compare_on_barabasi(n_nodes: int) -> tuple[str, Graph]:
    name = f"compare_on_barabasi_{n_nodes}_nodes_extended_path"

    setup = Graph(
        scenario=GraphScenario.BARABASI,
        params=BarabasiRadialParams(
            n_nodes=n_nodes,
            step_distance=15.0,
            reward_range=(10, 100),
            seed=42,
        ),
    )
    return name, setup


def run_group(name: str, experiments: list[Experiment]) -> None:
    print(f"🚀 Starting group process: {name}")
    ExperimentRunner.run_parallel(experiments=experiments, max_workers=2, reuse_graph=True)
    print(f"✅ Group finished: {name}")


def get_all_compare_on_barabasi_scenario() -> dict[str, list[Experiment]]:
    groups = {}
    for nodes in [20, 40, 60, 80, 100]:
        exp_name, graph_setup = get_compare_on_barabasi(nodes)
        groups[exp_name] = get_compare_on_scenarios_experiment(nodes // 2, exp_name, graph_setup)
    return groups


if __name__ == "__main__":
    all_compare_experiments = get_all_compare_on_barabasi_scenario()

    processes = []

    for name, experiments in all_compare_experiments.items():
        p = multiprocessing.Process(target=run_group, args=(name, experiments))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
