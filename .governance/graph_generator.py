import yaml
from pathlib import Path
import sys

# Assume run from repo root
CANON_PATH = Path("canon")
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"
OUTPUT_PATH = Path(".governance/constitutional_graph.dot")


class GraphGenerator:

    def __init__(self):
        self.axioms = self._load_semantic("axioms.yaml")["axioms"]
        self.intents = self._load_semantic("intents.yaml")["intents"]
        self.invariants = self._load_semantic("invariants.yaml")["invariants"]

        self.rules = self._load_rules()

    def _load_semantic(self, file):
        path = SEMANTIC_PATH / file
        if not path.exists():
             alt_path = Path(__file__).parent.parent / "canon" / "semantic" / file
             if alt_path.exists():
                 path = alt_path
        return yaml.safe_load(path.read_text())

    def _load_rules(self):
        rule_list = []
        path = RULES_PATH
        if not path.exists():
            path = Path(__file__).parent.parent / "canon" / "rules"

        for file in path.rglob("*.yaml"):
            data = yaml.safe_load(file.read_text())
            if data and "id" in data:
                rule_list.append(data)
        return rule_list

    # --------------------------------------------------

    def generate(self):
        lines = []
        lines.append("digraph ConstitutionalGraph {")
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=box];")

        # Axioms
        for ax in self.axioms:
            lines.append(
                f'  "{ax["id"]}" [shape=hexagon, style=filled, fillcolor=lightcoral];'
            )

        # Intents
        for intent in self.intents:
            lines.append(
                f'  "{intent["id"]}" [shape=ellipse, style=filled, fillcolor=lightblue];'
            )

        # Invariants
        for inv in self.invariants:
            lines.append(
                f'  "{inv["id"]}" [shape=box, style=filled, fillcolor=lightyellow];'
            )

        # Rules
        for rule in self.rules:
            lines.append(
                f'  "{rule["id"]}" [shape=diamond, style=filled, fillcolor=lightgray];'
            )

        # Edges: Axiom → Invariant
        for inv in self.invariants:
            for ax in inv.get("derives_from_axioms", []):
                lines.append(f'  "{ax}" -> "{inv["id"]}";')

        # Edges: Invariant → Intent
        for inv in self.invariants:
            for intent in inv.get("supports_intents", []):
                lines.append(f'  "{inv["id"]}" -> "{intent}";')

        # Edges: Rule → Invariant
        for inv in self.invariants:
            for rule in inv.get("enforces_rules", []):
                lines.append(f'  "{rule}" -> "{inv["id"]}";')

        lines.append("}")

        OUTPUT_PATH.write_text("\n".join(lines))
        print(f"✅ Constitutional graph written to {OUTPUT_PATH}")


if __name__ == "__main__":
    GraphGenerator().generate()
