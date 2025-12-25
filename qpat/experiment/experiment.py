from dataclasses import dataclass
from experiment.topology import Topology
from experiment.workflow import Workflow

@dataclass
class Experiment:
    topology: Topology
    workflow: Workflow