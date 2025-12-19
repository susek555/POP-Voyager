from typing import Any

type Position = tuple[float, float, float]
type NodeId = str
type NodeAttrs = dict[str, Any]
type EdgeAttrs = dict[str, float]
type NeighborMap = dict[str, list[str]]


type NodesData = list[tuple[NodeId, NodeAttrs]]
type EdgesData = list[tuple[NodeId, NodeId, EdgeAttrs]]
