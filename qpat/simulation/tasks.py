from dataclasses import dataclass
from typing import Callable, Tuple, Dict, Any


@dataclass
class SimulationTask:
    """
    A declarative instruction:
      - what function should be executed
      - when (relative time, in seconds)
      - with what arguments
    """
    target: str            # node name (e.g. "Source")
    method: str            # method name (e.g. "emit")
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = None
    time: int = 0      # ps (relative to timeline start)
