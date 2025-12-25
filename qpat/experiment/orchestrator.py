from typing import List
from qpat.experiment.workflow import Workflow
from qpat.capabilities.factory import CapabilityFactory

def _coerce_params(self, params: dict) -> dict:
    clean = {}
    for k, v in params.items():
        if isinstance(v, str):
            try:
                # Handles "1e-6", "8e7", "10e6", etc.
                clean[k] = float(v)
            except ValueError:
                clean[k] = v
        else:
            clean[k] = v
    return clean


class ExperimentOrchestrator:
    """
    Orchestrates experiments from topology + workflow.
    """

    def __init__(self, topology, workflow: Workflow):
        self.topology = topology
        self.workflow = workflow
        self.cap_factory = CapabilityFactory()

    def run(self):
        results = []

        for phase in self.workflow.phases:
            print(f"[Experiment] Phase '{phase.name}' started")

            for step in phase.steps:
                print(
                    f"[Experiment] Step: capability={step.capability}, "
                    f"params={step.params}"
                )

                # Create capability on demand
                capability = self.cap_factory.create(
                    step.capability,
                    topology=self.topology.clone(),  # important: isolation
                )

                # Execute experiment
                clean_params = _coerce_params(self, step.params)
                result = capability.run(**clean_params)
                results.append(result)

            print(f"[Experiment] Phase '{phase.name}' completed")

        return results
