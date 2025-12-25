import numpy as np
from numpy import dot
from typing import TYPE_CHECKING
from sequence.components.photon import Photon
from sequence.kernel.entity import Entity
from sequence.utils.encoding import polarization


if TYPE_CHECKING:
    from sequence.kernel.timeline import Timeline


class WavePlate(Entity):
    def __init__(self, name: str, timeline: "Timeline", plate_type="HWP", angle=0.0, encoding_type=polarization):
        super().__init__(name, timeline)
        assert plate_type in ["HWP", "QWP"], "Invalid wave plate type"
        self.plate_type = plate_type
        self.angle = angle
        self.encoding_type = encoding_type
        self.unitary = self._get_jones_matrix()
        self.unitary_signal = np.kron(self.unitary, np.identity(2))
        self.unitary_idler = np.kron(np.identity(2), self.unitary)

    def init(self):
        assert len(self._receivers) == 1
        pass

    def get(self, photon: Photon, **kwargs):
        #print(f"State before {self.name} ({self.plate_type} at {np.rad2deg(self.angle):.1f}°): {photon.quantum_state.state}")
        assert photon.encoding_type["name"] == self.encoding_type["name"]
        full_state = photon.quantum_state.state

        # Only handle 2D or 4D polarization vectors
        if len(full_state) == 2:
            # Single-photon polarization (e.g., before entanglement)
            new_state = tuple(dot(self.unitary, full_state))
            photon.set_state(new_state.tolist())
        elif len(full_state) == 4:
            if photon.name == "0":
                op = self.unitary_signal  # act on qubit 0
            elif photon.name == "1":
                op = self.unitary_idler  # act on qubit 1
            else:
                raise ValueError("For entangled states, specify photon name='0' or '1'")
            
            new_state = dot(op, full_state)
            photon.set_state(tuple(new_state))
            #print(f"State after {self.name} ({self.plate_type} at {np.rad2deg(self.angle):.1f}°): {photon.quantum_state.state}")

        else:
            raise ValueError("Unexpected photon state dimension")

        nxt = self._receivers[0]
        try:
            nxt.get(photon, **kwargs)
        except TypeError:
            nxt.get(photon)

    def set_angle(self, theta: float):
        self.angle = theta
        self.unitary = self._get_jones_matrix()
        self.unitary_signal = np.kron(self.unitary, np.identity(2))
        self.unitary_idler = np.kron(np.identity(2), self.unitary)

    def _get_jones_matrix(self):
        theta = self.angle
        c = np.cos(2 * theta)
        s = np.sin(2 * theta)

        if self.plate_type == "HWP":
            return np.array([[c, s], [s, -c]])
        if self.plate_type == "QWP":
            c = np.cos(theta)
            s = np.sin(theta)
            return np.array([
                [c**2 + 1j * s**2, (1 - 1j) * c * s],
                [(1 - 1j) * c * s, s**2 + 1j * c**2]
            ], dtype=complex)