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


class GraphParams:
    pass

@dataclass
class Graph:
    scenario: GraphScenario
    params: GraphParams

