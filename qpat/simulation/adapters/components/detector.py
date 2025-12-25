"""Models for photon detection devices.

This module models a single photon detector (SPD) for measurement of individual photons.
It also defines a QSDetector class,
which combines models of different hardware devices to measure photon states in different bases.
QSDetector is defined as an abstract template and as implementations for polarization and time bin qubits.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from numpy import eye, kron, exp, sqrt
from scipy.linalg import fractional_matrix_power
from math import factorial

from sequence.components.detector import QSDetector
from sequence.components.detector import Detector
from sequence.components.photon import Photon

from qpat.simulation.adapters.components.beam_splitter import FixedBasisBeamSplitter

if TYPE_CHECKING:
    from sequence.kernel.timeline import Timeline


class FixedBasisPolarizationDetector(QSDetector):
    """
    Polarization detector using a fixed-basis beam splitter.

    Attributes:
        detectors (list): Two detectors for orthogonal polarizations.
        splitter (FixedBasisBeamSplitter): Measures photons in a fixed polarization basis.
        trigger_times (list[list[int]]): List of detection timestamps for each detector.
    """

    def __init__(self, name: str, timeline: "Timeline", basis_index: int = 0):
        """
        Args:
            name (str): Component name.
            timeline (Timeline): Simulation timeline.
            basis_index (int): 0 for H/V basis, 1 for +/- diagonal basis.
        """
        super().__init__(name, timeline)

        self.detectors = []
        for i in range(2):
            d = Detector(f"{name}.detector{i}", timeline, efficiency=0.95, dark_count=500, time_resolution=150)
            d.attach(self)
            self.detectors.append(d)

        self.splitter = FixedBasisBeamSplitter(f"{name}.splitter", timeline, basis_index=basis_index)
        self.splitter.add_receiver(self.detectors[0])
        self.splitter.add_receiver(self.detectors[1])

        self.trigger_times = [[], []]
        self.components = [self.splitter] + self.detectors

    def init(self) -> None:
        assert len(self.detectors) == 2
        super().init()

    def get(self, photon: Photon, **kwargs) -> None:
        self.splitter.get(photon)

    def get_photon_times(self):
        times = self.trigger_times
        self.trigger_times = [[], []]
        return times

    # Dummy methods for compatibility
    def set_basis_list(self, *args, **kwargs): pass
    def update_splitter_params(self, *args, **kwargs): pass
