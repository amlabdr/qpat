from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from sequence.kernel.timeline import Timeline
from sequence.components.optical_channel import QuantumChannel

from qpat.experiment.topology import Topology
from qpat.experiment.specs import NodeSpec, QuantumLinkSpec

# Your concrete node implementations
from qpat.simulation.adapters.nodes.source_node import SpdcSourceNode
from qpat.simulation.adapters.nodes.polarization_measurement_node import PolarizationAnalyzer
from qpat.simulation.view import SimulationView


from sequence.kernel.process import Process
from sequence.kernel.event import Event


# --------------------------------------------------
# Returned container
# --------------------------------------------------

@dataclass
class SequenceTopology:
    timeline: Timeline
    nodes: Dict[str, object]   # Node subclasses

    # --------------------------------------------

    def schedule_tasks(self, tasks) -> None:
        """
        Translate SimulationTask → SeQUeNCe events.
        """
        for task in tasks:
            if task.target not in self.nodes:
                raise KeyError(f"Unknown node '{task.target}'")

            node = self.nodes[task.target]

            if not hasattr(node, task.method):
                raise AttributeError(
                    f"Node '{task.target}' has no method '{task.method}'"
                )

            process = Process(
                node,
                task.method,
                list(task.args),
            )

            event = Event(task.time, process)
            self.timeline.schedule(event)

# --------------------------------------------------
# Builder
# --------------------------------------------------

class SequenceTopologyBuilder:
    """
    Translate a declarative Topology into concrete SeQUeNCe objects.

    Optical and source implementations are delegated to node classes.
    """

    def build(self, topology: Topology) -> SequenceTopology:
        timeline = Timeline()
        nodes: Dict[str, object] = {}

        # ---- build nodes ----
        for name, spec in topology.nodes.items():
            nodes[name] = self._build_node(spec, timeline)

        # ---- build links ----
        for link in topology.links:
            self._build_link(link, nodes, timeline)

        return SequenceTopology(
            timeline=timeline,
            nodes=nodes,
        )

    # --------------------------------------------------

    def _build_node(self, spec: NodeSpec, timeline: Timeline):
        """
        Instantiate concrete SeQUeNCe nodes based on semantic role.
        """

        if spec.role == "source":
            # Default SPDC config (can be parameterized later)
            return SpdcSourceNode(
                name=spec.name,
                timeline=timeline,
                config=spec.params
            )

        elif spec.role == "polarization_measurement":
            return PolarizationAnalyzer(
                name=spec.name,
                timeline=timeline,
            )

        else:
            raise ValueError(f"Unknown node role: {spec.role}")

    # --------------------------------------------------

    def _build_link(
        self,
        spec: QuantumLinkSpec,
        nodes: Dict[str, object],
        timeline: Timeline,
    ):
        qc = QuantumChannel(
            name=f"qc_{spec.src}_{spec.dst}",
            timeline=timeline,
            distance=spec.distance,
            attenuation=spec.attenuation,
        )

        qc.set_ends(nodes[spec.src], nodes[spec.dst].name)
