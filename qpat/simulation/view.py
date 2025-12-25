# qpat/simulation/view.py
from typing import Dict, List

class SimulationView:
    """
    Read-only view of simulation results.
    Simulator-agnostic.
    """

    def __init__(self, detections: Dict[str, List[float]]):
        self._detections = detections

    def detection_times(self, node_name: str):
        return self._detections.get(node_name, [])