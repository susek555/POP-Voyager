from typing import Any, TypeAlias, TypedDict

Position: TypeAlias = tuple[float, float, float]
NodeId: TypeAlias = str
NodeAttrs: TypeAlias = dict[str, Any]
EdgeAttrs: TypeAlias = dict[str, float]


NodesData: TypeAlias = list[tuple[NodeId, NodeAttrs]]
EdgesData: TypeAlias = list[tuple[NodeId, NodeId, EdgeAttrs]]
