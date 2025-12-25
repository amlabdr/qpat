from abc import ABC, abstractmethod
from qpat.simulation.engine import SimulationEngine
from qpat.simulation.tasks import SimulationTask



class CapabilityResult:
    def __init__(self, value, metadata=None):
        self.value = value
        self.metadata = metadata or {}


class Capability(ABC):
    """
    One independent experiment.
    """

    def __init__(self, topology, builder):
        self.topology = topology
        self.builder = builder

    @abstractmethod
    def run(self, **params) -> CapabilityResult:
        pass

    def _run_engine(self, duration: float, tasks: list[SimulationTask]):
        engine = SimulationEngine(
            topology=self.topology,
            topology_builder=self.builder,
        )

        sim = engine.run(duration, tasks=tasks)

        return sim
