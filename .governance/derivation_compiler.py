import yaml
from pathlib import Path
import sys
from governance_lattice import get_sage_root

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"


class DerivationCompiler:

    def __init__(self):
        self.axioms = self._load_semantic("axioms.yaml")["axioms"]
        self.intents = self._load_semantic("intents.yaml")["intents"]
        self.invariants = self._load_semantic("invariants.yaml")["invariants"]

        self._load_rules_and_additional_invariants()

        self._index()

    def _load_semantic(self, file):
        path = SEMANTIC_PATH / file
        if not path.exists():
             alt_path = Path(__file__).parent.parent / "canon" / "semantic" / file
             if alt_path.exists():
                 path = alt_path
        return yaml.safe_load(path.read_text())

    # --------------------------------------------------

    def _load_rules_and_additional_invariants(self):
        self.rules = {}
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
                    self.rules[item["id"]] = item
                elif item.get("type") == "invariant":
                    self.invariants.append(item)

    def _index(self):
        self.axiom_ids = {a["id"] for a in self.axioms}
        self.intent_ids = {i["id"] for i in self.intents}
        self.invariant_ids = {inv["id"] for inv in self.invariants}
        self.rule_ids = set(self.rules.keys())

    # --------------------------------------------------

    def analyze(self):
        print("🔎 Derivation Analysis Report\n")

        self._detect_orphan_rules()
        self._detect_unprotected_intents()
        self._detect_unenforced_invariants()
        self._detect_unanchored_intents()
        self._detect_unanchored_invariants()

    # --------------------------------------------------

    def _detect_orphan_rules(self):
        enforced = set()

        for inv in self.invariants:
            for rule_id in inv.get("enforces_rules", []):
                enforced.add(rule_id)

        orphan_rules = self.rule_ids - enforced

        if orphan_rules:
            print("⚠ Orphan Rules (not bound to invariants):")
            for r in sorted(list(orphan_rules)):
                print(f"  - {r}")
            print()

    # --------------------------------------------------

    def _detect_unprotected_intents(self):
        protected = set()

        for inv in self.invariants:
            for intent in inv.get("supports_intents", []):
                protected.add(intent)

        unprotected = self.intent_ids - protected

        if unprotected:
            print("⚠ Intents not protected by any invariant:")
            for i in sorted(list(unprotected)):
                print(f"  - {i}")
            print()

    # --------------------------------------------------

    def _detect_unenforced_invariants(self):
        unenforced = []

        for inv in self.invariants:
            if not inv.get("enforces_rules"):
                unenforced.append(inv["id"])

        if unenforced:
            print("⚠ Invariants without enforcing rules:")
            for inv in sorted(unenforced):
                print(f"  - {inv}")
            print()

    # --------------------------------------------------

    def _detect_unanchored_intents(self):
        anchored = set()

        for inv in self.invariants:
            for axiom in inv.get("derives_from_axioms", []):
                anchored.add(axiom)

        unanchored = self.axiom_ids - anchored

        if unanchored:
            print("⚠ Axioms not deriving any invariant:")
            for a in sorted(list(unanchored)):
                print(f"  - {a}")
            print()

    # --------------------------------------------------

    def _detect_unanchored_invariants(self):
        for inv in self.invariants:
            if not inv.get("derives_from_axioms"):
                print(f"⚠ Invariant {inv['id']} has no axiom anchor.")
        print()


if __name__ == "__main__":
    DerivationCompiler().analyze()
