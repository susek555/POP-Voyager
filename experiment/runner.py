import json
from dataclasses import dataclass

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
    experiment: Experiment

    def perform(self) -> None:
        G = call_generate_graph(self.experiment.graph)
        results = []
        for _ in range(self.experiment.times_to_run):
            results.append(self.run_once(G))
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
        filename = f"./experiments/results/{self.experiment.name}.json"

        results_dict = results.__dict__.copy()
        results_dict["best_path"] = list(results.best_path)

        data_to_save = {
            "experiment_name": self.experiment.name,
            "max_nodes": self.experiment.max_nodes,
            "graph": {
                "scenario": self.experiment.graph.scenario.name,
                "params": self.experiment.graph.params.__dict__,
            },
            "algorithm": {
                "type": self.experiment.algorithm.type.name,
                "params": self.experiment.algorithm.params.__dict__,
            },
            "result": results_dict,
        }
        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

