from qpat.capabilities.polarization_analysis import PolarizationAnalysisCapability
from qpat.analysis.coincidences.window_method import WindowCoincidenceModel
from qpat.simulation.adapters.sequence_adapter import SequenceTopologyBuilder


class CapabilityFactory:
    """
    Builds capabilities from workflow steps and topology.
    """

    def __init__(self):
        self.builder = SequenceTopologyBuilder()

    def create(self, capability_name: str, topology):
        """
        Create and configure a capability instance.
        """
        if capability_name == "polarization_analysis":
            return PolarizationAnalysisCapability(
                topology=topology,
                builder=self.builder,
                source_name="Source",
                alice_name="Alice",
                bob_name="Bob",
                coincidence_model=WindowCoincidenceModel(window=1e-9),
            )

        raise ValueError(f"Unknown capability '{capability_name}'")

    
