from abc import ABC, abstractmethod
from typing import Any, List


class CoincidenceModel(ABC):
    """
    Base interface for coincidence detection models.
    """

    @abstractmethod
    def compute(self, detection_events: List[dict]) -> Any:
        """
        Compute coincidences from detection events.
        """
        pass

    @abstractmethod
    def rate(self, coincidences: Any, duration: float) -> float:
        """
        Compute coincidence rate (Hz).
        """
        pass
