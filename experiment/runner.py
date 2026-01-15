import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from multiprocessing import Manager

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
    max_nodes: int
    times_to_run: int


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
            self.experiment.max_nodes,
            objective_function=objective_function,
        )
        time = timer.get_elapsed()
        score = objective_function(graph, path)
        return ExperimentResult(
            score=score,
            time=time,
            path=path,
        )

    def save_to_json(self, results: AgregatedExperimentResult) -> None:
        # 1. Przygotowanie ścieżki
        target_dir = "experiment/results"
        os.makedirs(target_dir, exist_ok=True)

        safe_name = self.experiment.name.replace("../", "").replace("./", "")
        filename = os.path.join(target_dir, f"{safe_name}.jsonl")

        best_path_nodes = (
            list(results.best_path.nodes)
            if hasattr(results.best_path, "nodes")
            else list(results.best_path)
        )

        data_to_save = {
            "experiment_name": self.experiment.name,
            "max_nodes": self.experiment.max_nodes,
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
        print(f"🚀 Starting {len(experiments)} experiments on {max_workers} workers...")

        with Manager() as manager:
            shared_lock = manager.Lock()

            common_graph = None
            if reuse_graph and experiments:
                common_graph = call_generate_graph(experiments[0].graph)

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(cls._worker_task, exp, shared_lock, common_graph)
                    for exp in experiments
                ]

                for future in as_completed(futures):
                    try:
                        name = future.result()
                        print(f"✅ Completed: {name}")
                    except Exception as e:
                        print(f"❌ Experiment ended with error: {e}")

    @staticmethod
    def _worker_task(exp: Experiment, lock: object, graph_obj: nx.Graph) -> str:
        runner = ExperimentRunner(experiment=exp, lock=lock, graph=graph_obj)
        runner.perform()
        return exp.name
