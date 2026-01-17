import contextlib
import json
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from enum import Enum

import networkx as nx

from experiment.calls import call_algorithm, call_generate_graph
from experiment.result import AgregatedExperimentResult, ExperimentResult
from experiment.timer import Timer
from graph.config import Graph
from objective_function import objective_function
from utils.config import Algorithm


@dataclass
class Experiment:
    name: str
    graph: Graph
    algorithm: Algorithm
    nodes: int
    times_to_run: int


def clean_types(obj: object) -> object:
    if isinstance(obj, Enum):
        return obj.name
    if hasattr(obj, "item"):
        return obj.item()
    if callable(obj):
        return getattr(obj, "__name__", str(obj))
    if isinstance(obj, dict):
        return {str(k): clean_types(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean_types(i) for i in obj]
    return obj


def _run_task_internal(exp_dict: dict, lock: object, graph_data: dict | None) -> str:
    import networkx as nx

    from experiment.runner import Experiment, ExperimentRunner
    from graph.config import Graph, GraphScenario
    from utils.a_star import AStarParams
    from utils.ant_colony.common import AcoParams
    from utils.config import Algorithm, AlgorithmType
    from utils.genetic import GeneticParams
    from utils.sa import SAparams

    try:
        algo_type = exp_dict["algorithm"]["type"]
        raw_params = exp_dict["algorithm"]["params"]

        if algo_type == AlgorithmType.SA or "SA" in str(algo_type):
            algo_params = SAparams(**raw_params)
        elif algo_type == AlgorithmType.GENETIC or "GENETIC" in str(algo_type):
            algo_params = GeneticParams(**raw_params)
        elif algo_type == AlgorithmType.ACO or "ACO" in str(algo_type):
            algo_params = AcoParams(**raw_params)
        elif algo_type == AlgorithmType.A_STAR or "A_STAR" in str(algo_type):
            algo_params = AStarParams(**raw_params)
        else:
            algo_params = raw_params

        scenario_data = exp_dict["graph"]["scenario"]
        if isinstance(scenario_data, str):
            scenario_enum = GraphScenario[scenario_data]
        else:
            scenario_enum = scenario_data

        exp_obj = Experiment(
            name=exp_dict["name"],
            nodes=exp_dict["nodes"],
            times_to_run=exp_dict["times_to_run"],
            graph=Graph(scenario=scenario_enum, params=exp_dict["graph"]["params"]),
            algorithm=Algorithm(type=algo_type, params=algo_params),
        )

        graph_obj = None
        if graph_data is not None:
            graph_obj = nx.node_link_graph(graph_data, edges="edges")

        runner = ExperimentRunner(experiment=exp_obj, lock=lock, graph=graph_obj)
        runner.perform()
        return exp_obj.name

    except Exception as e:
        import traceback

        return f"ERROR_IN_WORKER:{exp_dict.get('name')}:{str(e)}\n{traceback.format_exc()}"


@dataclass
class ExperimentRunner:
    experiment: Experiment = None
    graph: nx.Graph = None
    lock: object = None

    def update_experiment(self, experiment: Experiment, generate_new_graph: bool = False) -> None:
        self.experiment = experiment
        if generate_new_graph or self.graph is None:
            self.graph = call_generate_graph(self.experiment.graph)

    def perform(self) -> None:
        if not self.graph:
            self.graph = call_generate_graph(self.experiment.graph)
        results = []
        for _ in range(self.experiment.times_to_run):
            results.append(self.run_once(self.graph))
        agregated_results = AgregatedExperimentResult(results, self.experiment.times_to_run)
        self.save_to_json(agregated_results)

    def run_once(self, graph: nx.Graph) -> ExperimentResult:
        timer = Timer(call_algorithm)
        path = timer.run(
            self.experiment.algorithm,
            graph,
            self.experiment.nodes,
            objective_function=objective_function,
        )
        time = timer.get_elapsed()
        score = objective_function(graph, path)
        return ExperimentResult(score=score, time=time, path=path)

    def save_to_json(self, results: AgregatedExperimentResult) -> None:
        target_dir = "experiment/results"
        os.makedirs(target_dir, exist_ok=True)

        safe_name = self.experiment.name.replace("../", "").replace("./", "")
        filename = os.path.join(target_dir, f"{safe_name}.jsonl")

        best_path_nodes = (
            list(results.best_path.nodes)
            if hasattr(results.best_path, "nodes")
            else list(results.best_path)
        )

        data_to_save = clean_types(
            {
                "experiment_name": self.experiment.name,
                "max_nodes": self.experiment.nodes,
                "graph": {
                    "scenario": self.experiment.graph.scenario.name,
                    "params": self.experiment.graph.params.__dict__
                    if hasattr(self.experiment.graph.params, "__dict__")
                    else self.experiment.graph.params,
                },
                "algorithm": {
                    "type": self.experiment.algorithm.type.name,
                    "params": self.experiment.algorithm.params.__dict__
                    if hasattr(self.experiment.algorithm.params, "__dict__")
                    else self.experiment.algorithm.params,
                },
                "result": {
                    "average_score": round(float(results.average_score), 2),
                    "best_score": round(float(results.best_score), 2),
                    "worst_score": round(float(results.worst_score), 2),
                    "median_score": round(float(results.median_score), 2),
                    "std_dev_score": round(float(results.std_dev_score), 2),
                    "average_time": round(float(results.average_time), 2),
                    "best_time": round(float(results.best_time), 2),
                    "total_time": round(float(results.total_time), 2),
                    "best_path": best_path_nodes,
                    "runs_count": int(results.runs_count),
                },
            }
        )
        json_line = json.dumps(data_to_save) + "\n"

        if self.lock:
            with self.lock, open(filename, "a", encoding="utf-8") as f:
                f.write(json_line)
        else:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(json_line)

    @classmethod
    def run_parallel(
        cls, experiments: list[Experiment], max_workers: int = 4, reuse_graph: bool = False
    ) -> None:
        with contextlib.suppress(RuntimeError):
            multiprocessing.set_start_method("spawn", force=True)

        print(f"🚀 Starting {len(experiments)} experiments on {max_workers} workers...")

        with multiprocessing.Manager() as manager:
            shared_lock = manager.Lock()

            common_graph_data = None
            if reuse_graph and experiments:
                g = call_generate_graph(experiments[0].graph)
                common_graph_data = nx.node_link_data(g, edges="edges")

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(_run_task_internal, asdict(exp), shared_lock, common_graph_data)
                    for exp in experiments
                ]

                for future in as_completed(futures):
                    try:
                        res = future.result()
                        if res.startswith("ERROR"):
                            print(f"❌ {res}")
                        else:
                            print(f"✅ Completed: {res}")
                    except Exception as e:
                        print(f"💀 Critical Pool Error: {e}")
