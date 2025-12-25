from dataclasses import dataclass, field
from typing import Dict, List
import copy

from qpat.experiment.specs import NodeSpec, QuantumLinkSpec


@dataclass
class Topology:
    nodes: Dict[str, NodeSpec] = field(default_factory=dict)
    links: List[QuantumLinkSpec] = field(default_factory=list)

    def add_node(self, node: NodeSpec):
        if node.name in self.nodes:
            raise ValueError(f"Node '{node.name}' already exists")
        self.nodes[node.name] = node

    def add_link(self, link: QuantumLinkSpec):
        self.links.append(link)
    
    def clone(self) -> "Topology":
        """
        Return a deep copy of the topology so each experiment
        runs in full isolation.
        """
        return copy.deepcopy(self)
