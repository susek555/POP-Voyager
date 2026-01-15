from dataclasses import dataclass

import numpy as np

from models.path import Path


@dataclass
class ExperimentResult:
    score: float
    time: float
    path: Path


@dataclass
class AgregatedExperimentResult:
    average_score: float
    best_score: float
    worst_score: float
    median_score: float
    std_dev_score: float

    average_time: float
    best_time: float
    total_time: float

    best_path: Path

    runs_count: int

    def __init__(self, results: list[ExperimentResult], n_iter: int) -> None:
        scores = [result.score for result in results]
        times = [result.time for result in results]

        self.average_score = float(np.mean(scores))
        self.best_score = float(np.max(scores))
        self.worst_score = float(np.min(scores))
        self.median_score = float(np.median(scores))
        self.std_dev_score = float(np.std(scores))

        self.average_time = float(np.mean(times))
        self.best_time = float(np.min(times))
        self.total_time = float(np.sum(times))

        best_idx = scores.index(self.best_score)
        self.best_path = results[best_idx].path

        self.runs_count = n_iter
