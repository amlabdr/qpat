"""Models for simulation of a polarization beam splitter.

This module defines the class BeamSplitter, which is used for simulating polarization beam splitters. 
The beam splitter receives photons with polarization encoding and forwards photons to one of two 
attached receivers (which can be any entity).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sequence.kernel.timeline import Timeline
    from sequence.topology.node import Node

from numpy import trace

from sequence.components.photon import Photon
from sequence.kernel.entity import Entity
from sequence.utils.encoding import polarization


class FixedBasisBeamSplitter(Entity):
    """
    A simplified beam splitter that always measures in a fixed polarization basis.
    """

    def __init__(self, name: str, timeline, basis_index: int = 0, fidelity: float = 1.0, mismeasure_prob: float = 0.0):
        """
        Args:
            name (str): name of the beam splitter.
            timeline (Timeline): the simulation timeline.
            basis_index (int): index of the polarization basis (0 for H/V, 1 for +/-).
            fidelity (float): probability of transmitting a received photon.
        """
        super().__init__(name, timeline)
        self.fidelity = fidelity
        self.basis_index = basis_index  # 0: H/V, 1: diagonal
        self.mismeasure_prob = mismeasure_prob
        self._receivers = []  # will be filled externally

    def init(self):
        assert len(self._receivers) == 2, "BeamSplitter requires exactly 2 receivers."

    def get(self, photon: Photon, **kwargs):
        assert photon.encoding_type["name"] == "polarization", "Photon must be polarization encoded."

        if self.get_generator().random() < self.fidelity:
            # Perform measurement in fixed basis
            basis = polarization["bases"][self.basis_index]
            result = Photon.measure(basis, photon, self.get_generator())
            # Flip the result with mismeasure_prob
            if self.get_generator().random() < self.mismeasure_prob:
                result = 1 - result  # Flip 0 ↔ 1
            self._receivers[result].get(photon)

            