from abc import ABC, abstractmethod
from dataclasses import dataclass

from .common import AcoParams, AcoState


class StagnationStrategy(ABC):
    @abstractmethod
    def should_act(self, state: AcoState) -> bool:
        """Determine whether the strategy should perform its action."""
        ...

    @abstractmethod
    def execute(self, state: AcoState, params: AcoParams) -> None:
        """Perform the strategy action to counter stagnation"""
        ...

    @abstractmethod
    def should_stop(self, state: AcoState) -> tuple[bool, str]:
        """
        Check whether the algorithm should stop early because of unrecoverable stagnation

        Returns (should_stop, reason).
        """
        ...


@dataclass
class NoStrategy(StagnationStrategy):
    def should_act(self, state: AcoState) -> bool:
        return False

    def execute(self, state: AcoState, params: AcoParams) -> None:
        pass

    def should_stop(self, state: AcoState) -> tuple[bool, str]:
        return False, ""


@dataclass
class EarlyStoppingStrategy(StagnationStrategy):
    """Stop after N iterations without improvement"""

    patience: int = 100

    def should_act(self, state: AcoState) -> bool:
        return False

    def execute(self, state: AcoState, params: AcoParams) -> None: ...

    def should_stop(self, state: AcoState) -> tuple[bool, str]:
        if state.no_improvement_count >= self.patience:
            return True, f"Early stopping: no improvement for {self.patience} iterations"
        return False, ""
