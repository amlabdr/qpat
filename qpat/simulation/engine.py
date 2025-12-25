# qpat/simulation/engine.py
from __future__ import annotations
from typing import Any, Generator, Optional

from qpat.simulation.tasks import SimulationTask



class SimulationEngine:
    """
    High-level simulation orchestrator.

    Responsibilities:
      - Build simulation topology from experiment topology
      - Run the simulation timeline
    """

    def __init__(
        self,
        topology,
        topology_builder,
    ):
        self.topology_spec = topology
        self.builder = topology_builder

        self._sim_topology = None

    def build(self):
        if self._sim_topology is not None:
            return

        # Build simulator-specific topology (e.g. SeQUeNCe)
        self._sim_topology = self.builder.build(self.topology_spec)

    def run(self, duration: float, tasks: list[SimulationTask]):
        """
        Blocking run for a given duration.
        """
        self.build()
        assert self._sim_topology is not None

        sim = self._sim_topology
        timeline = sim.timeline

        sim.schedule_tasks(tasks)
        timeline.stop_time = duration

        # Run the simulation
        if hasattr(timeline, "init"):
            timeline.init()
        timeline.run()
        print("Finished")

        return sim
