from dataclasses import dataclass
from enum import Enum


class GraphScenario(Enum):
    BASIC = "basic"
    ARCHIPELAGO = "archipelago"
    BOTTLENECK = "bottleneck"
    GRADIENT = "gradient"
    LINE_CIRCLE = "line_circle"
    NEBULA = "nebula"
    SIREN_SONG = "siren_song"

@dataclass
class GraphParams:
    seed: int = 42

@dataclass
class Graph:
    scenario: GraphScenario
    params: GraphParams

