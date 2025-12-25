from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Literal


# -------------------------
# Base spec (NOT a dataclass)
# -------------------------

class Spec:
    """
    Base class for all specs.
    Holds optional metadata.
    """
    def __init__(self, metadata=None):
        self.metadata = metadata or {}


# -------------------------
# Node spec (ROLE-BASED)
# -------------------------

NodeRole = Literal[
    "source",
    "polarization_measurement",
]


@dataclass
class NodeSpec(Spec):
    """
    Declarative node specification.

    The role determines internal structure, which is instantiated
    by the simulation adapter (e.g., SeQUeNCe).
    """
    name: str
    role: NodeRole
    params: Dict[str, Any] = field(default_factory=dict)


# -------------------------
# Quantum link spec
# -------------------------

@dataclass
class QuantumLinkSpec(Spec):
    src: str
    dst: str

    distance: float = 0.0          # meters
    attenuation: float = 0.0       # dB/m

    model: Literal["ideal", "bifrost"] = "ideal"
    model_params: Dict[str, Any] = field(default_factory=dict)
