"""
Test: load topology YAML from local directory and inspect parsed objects.

Run:
  cd examples
  python test_load_topology.py
"""



from qpat.experiment.parser import load_topology_yaml


def main():
    filename = "examples/topology_min.yaml"

    print(f"[1] Loading topology from '{filename}'")
    topo = load_topology_yaml(filename)

    print("[2] Parsed nodes:")
    for name, node in topo.nodes.items():
        print(f"  - {name} (role={node.role})")
        if node.analyzer:
            print(
                f"      analyzer: "
                f"HWP={node.analyzer.hwp_angle}, "
                f"QWP={node.analyzer.qwp_angle}"
            )
        if node.detector:
            print(
                f"      detector: "
                f"eff={node.detector.efficiency}, "
                f"jitter={node.detector.jitter}"
            )
        if node.source:
            print(
                f"      source: "
                f"freq={node.source.frequency}, "
                f"μ={node.source.mean_photon_num}"
            )

    print("\n[3] Parsed links:")
    for link in topo.links:
        print(
            f"  - {link.src} -> {link.dst} "
            f"(distance={link.distance}, loss={link.loss})"
        )

    print("\n Topology YAML parsed correctly.")


if __name__ == "__main__":
    main()
