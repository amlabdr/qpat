from sequence.topology.node import Node
from qpat.simulation.adapters.components.detector import FixedBasisPolarizationDetector
from qpat.simulation.adapters.components.wave_plate import WavePlate
import numpy as np


class PolarizationAnalyzer(Node):
    """
    Component that models a polarization analyzer: 
    A half-wave plate followed by a polarization-sensitive detector.
    
    Attributes:
        wp (WavePlate): half-wave plate used to rotate polarization basis.
        detector (QSDetectorPolarization): polarization detector with two outputs.
    """

    def __init__(self, name: str, timeline):
        super().__init__(name, timeline)

        # QWP first (default physical angle 0 rad)
        self.qwp = WavePlate(f"{name}_QWP", timeline, plate_type="QWP", angle=0.0)

        # Half-Wave Plate
        self.hwp = WavePlate(f"{name}_HWP", timeline, "HWP", angle=0.0)
        
        # Polarization-sensitive QSDetector
        self.detector = FixedBasisPolarizationDetector(f"{name}_detector", timeline, basis_index = 0)

        # Wire-up: QWP -> HWP -> Detector
        self.hwp.add_receiver(self.qwp)
        self.qwp.add_receiver(self.detector)

        # Register components
        self.add_component(self.qwp)
        self.add_component(self.hwp)
        self.add_component(self.detector)
        self.add_component(self)
        self.set_first_component(self.name)
        
    def init(self):
        self.qwp.init()
        self.hwp.init()
        self.detector.init()

    def get(self, photon, **kwargs):
        """Receive photon and pass it through QWP"""
        print("Got photon")
        self.hwp.get(photon)

    # ------------- Convenience API -------------
    def set_qwp_angle(self, theta_rad: float):
        """Set QWP physical angle (radians)."""
        self.qwp.set_angle(theta_rad)

    def set_hwp_angle(self, theta_rad: float):
        """Set HWP physical angle (radians)."""
        self.hwp.set_angle(theta_rad)

    def set_basis(self, basis: str):
        """
        Set analyzer to measure one of the Pauli bases at the PBS:
          'Z' (H/V) : QWP=0°,   HWP=0°
          'X' (D/A) : QWP=0°,   HWP=22.5°
          'Y' (R/L) : QWP=45°,  HWP=0°
        Angles are physical plate angles.
        """
        b = basis.upper()
        if b == "Z":
            self.set_qwp_angle(0.0)
            self.set_hwp_angle(0.0)
        elif b == "X":
            self.set_qwp_angle(0.0)
            self.set_hwp_angle(np.deg2rad(22.5))
        elif b == "Y":
            self.set_qwp_angle(np.deg2rad(45.0))
            self.set_hwp_angle(0.0)
        else:
            raise ValueError("Unknown basis. Use 'Z', 'X', or 'Y'.")

    def get_detection_counts(self):
        """Returns the number of detections on each detector."""
        return self.detector.get_photon_times()