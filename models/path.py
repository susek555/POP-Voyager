from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Self, overload


@dataclass
class Path:
    path: list[str] = field(default_factory=list)

    @overload
    def __getitem__(self, index: int) -> str: ...

    @overload
    def __getitem__(self, index: slice) -> list[str]: ...

    def __getitem__(self, index):
        return self.path[index]

    @overload
    def __setitem__(self, index: int, value: str) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: list[str]) -> None: ...

    def __setitem__(self, index, value):
        self.path[index] = value

    def __iadd__(self, new_node: str) -> Self:
        self.path.append(new_node)
        return self

    def __add__(self, new_node: str) -> "Path":
        return Path(self.path + [new_node])

    def __len__(self) -> int:
        return len(self.path)

    def __iter__(self) -> Iterator[str]:
        return iter(self.path)
