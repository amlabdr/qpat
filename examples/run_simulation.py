from qpat.experiment.workflow_parser import load_workflow_yaml
from qpat.experiment.orchestrator import ExperimentOrchestrator
from qpat.experiment.parser import load_topology_yaml

topology = load_topology_yaml("examples/topology.yaml")
workflow = load_workflow_yaml("examples/workflow.yaml")

experiment = ExperimentOrchestrator(
    topology=topology,
    workflow=workflow,
)

results = experiment.run()

for r in results:
    print("Coincidence rate:", r.value)
