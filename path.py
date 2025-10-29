from dataclasses import dataclass
from typing import Iterator

@dataclass
class Path:
    path: list[str] = None

    def __getitem__(self, index):
        return self.path[index]


