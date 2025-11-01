from dataclasses import dataclass
from typing import Iterator


@dataclass
class Path:
    path: list[str] = None

    def __getitem__(self, index):
        return self.path[index]

    def __iadd__(self, new_node: str):
        self.path.append(new_node)
        return self

    def __add__(self, new_node: str):
        return Path(self.path + [new_node])
