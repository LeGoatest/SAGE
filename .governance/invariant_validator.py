import yaml
from pathlib import Path
import sys
from governance_lattice import get_sage_root

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"


class InvariantValidator:

    def __init__(self):
        self.axioms = self._load("axioms.yaml")["axioms"]
        self.intents = self._load("intents.yaml")["intents"]
        self.invariants = self._load("invariants.yaml")["invariants"]
        self.dependencies = self._load("dependencies.yaml")["dependencies"]

        self.rules = []
        self._load_rules_and_additional_invariants()

        self._index_data()

    def _load(self, file):
        path = SEMANTIC_PATH / file
        if not path.exists():
             # Fallback if run from .governance or tools
             alt_path = Path(__file__).parent.parent / "canon" / "semantic" / file
             if alt_path.exists():
                 path = alt_path
        return yaml.safe_load(path.read_text())

    def _load_rules_and_additional_invariants(self):
        path = RULES_PATH
        if not path.exists():
            path = Path(__file__).parent.parent / "canon" / "rules"

        for file in path.rglob("*.yaml"):
            data = yaml.safe_load(file.read_text())
            if not data:
                continue

            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict) or "id" not in item:
                    continue

                if item.get("type", "rule") == "rule":
                    self.rules.append(item["id"])
                elif item.get("type") == "invariant":
                    self.invariants.append(item)

    def _index_data(self):
        self.axiom_ids = {a["id"] for a in self.axioms}
        self.intent_ids = {i["id"] for i in self.intents}
        self.invariant_ids = {inv["id"] for inv in self.invariants}

    # --------------------------------------------------
    # PUBLIC VALIDATION ENTRY
    # --------------------------------------------------

    def validate(self):
        self._validate_invariant_references()
        self._validate_dependency_links()
        self._validate_orphans()
        print("✅ Invariant consistency validation passed.")

    # --------------------------------------------------
    # VALIDATION RULES
    # --------------------------------------------------

    def _validate_invariant_references(self):
        for inv in self.invariants:

            # Check rule references
            for rule_id in inv.get("enforces_rules", []):
                if rule_id not in self.rules:
                    self._fail(f"Invariant {inv['id']} references missing rule {rule_id}")

            # Check intent references
            for intent_id in inv.get("supports_intents", []):
                if intent_id not in self.intent_ids:
                    self._fail(f"Invariant {inv['id']} references missing intent {intent_id}")

            # Check axiom references
            for axiom_id in inv.get("derives_from_axioms", []):
                if axiom_id not in self.axiom_ids:
                    self._fail(f"Invariant {inv['id']} references missing axiom {axiom_id}")

    def _validate_dependency_links(self):
        axioms_to_intents = self.dependencies.get("axioms_to_intents", {})
        intents_to_invariants = self.dependencies.get("intents_to_invariants", {})

        # Validate axiom → intent links
        for axiom_id, intent_list in axioms_to_intents.items():
            if axiom_id not in self.axiom_ids:
                self._fail(f"Dependency references missing axiom {axiom_id}")
            for intent_id in intent_list:
                if intent_id not in self.intent_ids:
                    self._fail(f"Dependency references missing intent {intent_id}")

        # Validate intent → invariant links
        for intent_id, invariant_list in intents_to_invariants.items():
            if intent_id not in self.intent_ids:
                self._fail(f"Dependency references missing intent {intent_id}")
            for invariant_id in invariant_list:
                if invariant_id not in self.invariant_ids:
                    self._fail(f"Dependency references missing invariant {invariant_id}")

    def _validate_orphans(self):
        # Every invariant must support at least one intent
        for inv in self.invariants:
            if not inv.get("supports_intents"):
                self._fail(f"Invariant {inv['id']} has no supported intent")

        # Every invariant must derive from at least one axiom
        for inv in self.invariants:
            if not inv.get("derives_from_axioms"):
                self._fail(f"Invariant {inv['id']} has no axiom derivation")

    def _fail(self, message):
        print(f"❌ Invariant consistency error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    validator = InvariantValidator()
    validator.validate()
