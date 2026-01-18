from dataclasses import dataclass
from enum import Enum


class AlgorithmType(Enum):
    RANDOM = "random"
    GREEDY = "greedy"
    A_STAR = "a_star"
    SA = "simulated_annealing"
    GENETIC = "genetic"
    ACO = "ant_colony_optimization"


@dataclass
class AlgorithmParams:
    seed: int = 42

@dataclass
class Algorithm:
    type: AlgorithmType
    params: AlgorithmParams

