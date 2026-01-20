import random
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, cast

from models.graph import NodesData
from models.path import Path
from utils.config import AlgorithmParams


@dataclass(kw_only=True)
class GeneticParams(AlgorithmParams):
    pop_size: int
    generations: int
    mutation_rate: float
    crossover: Callable[[Path, Path, random.Random], tuple[Path, Path]]
    selection: Callable[[list[Path], list[float], int, random.Random], Path]
    selection_kwargs: dict[str, Any] = field(default_factory=dict)
    no_improvement_stop: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "pop_size": self.pop_size,
            "generations": self.generations,
            "mutation_rate": self.mutation_rate,
            "crossover": self.crossover.__name__,
            "selection": self.selection.__name__,
            "selection_kwargs": self.selection_kwargs,
            "no_improvement_stop": self.no_improvement_stop,
        }


def get_best_path_info(paths: list[Path], fitness: list[float]) -> tuple[Path, float]:
    best_idx = max(range(len(fitness)), key=fitness.__getitem__)
    best_path = paths[best_idx]
    best_score = fitness[best_idx]
    return best_path, best_score


def ordered_crossover(p1: Path, p2: Path, rng: random.Random) -> tuple[Path, Path]:
    start, end = 1, len(p1) - 1
    i, j = sorted(rng.sample(range(start, end), 2))

    o1: list[str | None] = [None] * len(p1)
    o2: list[str | None] = [None] * len(p1)

    o1[0] = o1[-1] = o2[0] = o2[-1] = "P"

    o1[i:j] = p1[i:j]
    o2[i:j] = p2[i:j]

    def fill_offspring(offspring: list[str | None], parent: list[str] | Path) -> None:
        parent_pos = j
        offspring_pos = j
        while None in offspring:
            if parent[parent_pos] not in offspring and parent[parent_pos] != "P":
                if offspring[offspring_pos] == "P":
                    offspring_pos += 1
                    offspring_pos %= len(parent)
                    continue

                offspring[offspring_pos] = parent[parent_pos]
                offspring_pos += 1
                offspring_pos %= len(parent)

            parent_pos += 1
            parent_pos %= len(parent)

    fill_offspring(o1, p2)
    fill_offspring(o2, p1)

    return Path(cast(list[str], o1)), Path(cast(list[str], o2))


def select_tournament(
    population: list[Path],
    fitness: list[float],
    tournament_size: int,
    rng: random.Random,
) -> Path:
    competitors = rng.sample(list(zip(population, fitness, strict=True)), k=tournament_size)
    winner = max(competitors, key=lambda x: x[1])[0]
    return winner


def mutate(path: Path, rng: random.Random) -> None:
    if len(path) <= 3:
        return
    i, j = rng.sample(range(1, len(path) - 1), 2)
    path[i], path[j] = path[j], path[i]


def get_random_path_no_duplicates(
    nodes_data: NodesData, number_of_nodes: int, rng: random.Random
) -> Path:
    available_nodes = [n for n, _ in nodes_data[1:]]
    chosen_nodes = rng.sample(available_nodes, k=min(number_of_nodes, len(available_nodes)))
    rng.shuffle(chosen_nodes)
    return Path(["P"] + chosen_nodes + ["P"])
