from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Step:
    capability: str
    params: Dict[str, Any]

@dataclass
class Phase:
    name: str
    steps: List[Step]


@dataclass
class Workflow:
    phases: List[Phase]
