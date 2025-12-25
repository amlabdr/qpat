"""
Minimal integration test for QPat simulation layer.

Pipeline:
  YAML -> Topology -> SequenceTopologyBuilder -> SimulationEngine -> run
"""

from qpat.experiment.parser import load_topology_yaml
from qpat.simulation.engine import SimulationEngine
from qpat.simulation.adapters.sequence_adapter import SequenceTopologyBuilder


def main():
    # 1) Load topology from YAML
    topo = load_topology_yaml("examples/topology_min.yaml")
    print("[OK] Topology loaded")
    print("  Nodes:", list(topo.nodes.keys()))
    print("  Links:", [(l.src, l.dst) for l in topo.links])

    # 2) Build simulation engine
    builder = SequenceTopologyBuilder()
    engine = SimulationEngine(
        topology=topo,
        topology_builder=builder,
    )
    print("[OK] SimulationEngine created")

    # 3) Run a short simulation
    duration = 1e-6  # 1 microsecond
    print(f"[RUN] Running simulation for {duration} s")
    engine.run(duration)

    print("[DONE] Simulation finished successfully")


if __name__ == "__main__":
    main()
