from qpat.capabilities.base import Capability, CapabilityResult
from qpat.analysis.coincidences.base import CoincidenceModel
from qpat.simulation.tasks import SimulationTask



class PolarizationAnalysisCapability(Capability):
    """
    Polarization Analysis with coincidences measurement capability.
    """

    name = "polarization_analysis"

    def __init__(
        self,
        topology,
        builder,
        source_name: str,
        alice_name: str,
        bob_name: str,
        coincidence_model: CoincidenceModel,
    ):
        super().__init__(topology, builder)

        self.source_name = source_name
        self.alice_name = alice_name
        self.bob_name = bob_name
        self.coincidence_model = coincidence_model

    def run(
        self,
        alice_angle: float,
        bob_angle: float,
        emission_time: float,
        frequency: float,
    ) -> CapabilityResult:
        """
        Run polarization coincidence measurement.

        Args:
            alice_angle: analyzer angle at Alice
            bob_angle: analyzer angle at Bob
            emission_time: seconds
            frequency: source emission frequency (Hz)
        """

        # ---- 1. Configure analyzers ----
        self.topology.nodes[self.alice_name].params["hwp_angle"] = alice_angle
        self.topology.nodes[self.bob_name].params["hwp_angle"] = bob_angle

        # ---- 2. Configure source ----
        self.topology.nodes[self.source_name].params["frequency"] = frequency

        num_pulses = int(emission_time) * int(frequency)

        tasks = [
            SimulationTask(
                target=self.source_name,
                method="emit",
                args=(num_pulses,),
                time=0.0,
            ),
        ]

        # ---- 3. Run simulation ----
        sim_topology = self._run_engine(duration=emission_time*1e12, tasks=tasks,)
        # ---- 4. Extract detection events from detectors ----
        alice_times = sim_topology.nodes[self.alice_name].get_detection_counts()
        bob_times   = sim_topology.nodes[self.bob_name].get_detection_counts()

        counts_A = alice_times
        counts_B = bob_times
        print(f"Counts A: {len(counts_A[0]+counts_A[1])}")
        print(f"Counts B: {len(counts_B[0])}")

        # 4. Offline coincidence analysis
        coincidences = self.coincidence_model.compute(alice_times, bob_times)
        rate = self.coincidence_model.rate(coincidences, emission_time)

        return CapabilityResult(rate)
