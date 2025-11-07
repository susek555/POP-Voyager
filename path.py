from dataclasses import dataclass, field


@dataclass
class Path:
    path: list[str] = field(default_factory=list)

    def __getitem__(self, index):
        return self.path[index]

    def __setitem__(self, index, value: str):
        self.path[index] = value

    def __iadd__(self, new_node: str):
        self.path.append(new_node)
        return self

    def __add__(self, new_node: str):
        return Path(self.path + [new_node])

    def __len__(self):
        return len(self.path)
