from __future__ import annotations

import yaml

from qpat.experiment.topology import Topology
from qpat.experiment.specs import NodeSpec, QuantumLinkSpec


def load_topology_yaml(path: str) -> Topology:
    """
    Load a topology YAML file and return a Topology object.

    Only semantic node roles are parsed here.
    """
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)

    topo_cfg = cfg.get("topology", {})
    topo = Topology()

    # ---- nodes ----
    for n in topo_cfg.get("nodes", []):
        node = NodeSpec(
            name=n["name"],
            role=n["role"],
            params=n.get("params", {}) or {},
        )
        topo.add_node(node)

    # ---- links ----
    for l in topo_cfg.get("links", []):
        link = QuantumLinkSpec(
            src=l["src"],
            dst=l["dst"],
            distance=float(l.get("distance", 0.0)),
            attenuation=float(l.get("attenuation", 0.0)),
            model=l.get("model", "ideal"),
            model_params=l.get("model_params", {}) or {},
        )
        topo.add_link(link)

    return topo
