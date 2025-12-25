import yaml
from qpat.experiment.workflow import Workflow, Phase, Step


def load_workflow_yaml(path: str) -> Workflow:
    """
    Load a workflow YAML file into a Workflow object.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if "workflow" not in data:
        raise ValueError("Missing 'workflow' section in YAML")

    phases = []

    for p in data["workflow"].get("phases", []):
        steps = []

        for s in p.get("steps", []):
            if "capability" not in s:
                raise ValueError("Workflow step missing 'capability' field")

            steps.append(
                Step(
                    capability=s["capability"],
                    params=s.get("params", {}),
                )
            )

        phases.append(
            Phase(
                name=p.get("name", "unnamed_phase"),
                steps=steps,
            )
        )

    return Workflow(phases=phases)
