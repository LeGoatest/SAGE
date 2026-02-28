import yaml
from pathlib import Path
import sys
from governance_lattice import get_sage_root

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"


class SemanticConflictValidator:

    def __init__(self):
        self.invariants = self._load_semantic("invariants.yaml")["invariants"]
        self.intents = self._load_semantic("intents.yaml")["intents"]
        self.axioms = self._load_semantic("axioms.yaml")["axioms"]

        self.rules = {}
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
        self.intent_ids = {i["id"] for i in self.intents}
        self.axiom_ids = {a["id"] for a in self.axioms}
        self.rule_ids = set(self.rules.keys())

    # --------------------------------------------------

    def validate(self):
        self._detect_rule_conflicts()
        self._detect_invariant_self_conflicts()
        self._detect_axiom_conflicts()
        print("✅ Semantic conflict validation passed.")

    # --------------------------------------------------
    # Conflict Checks
    # --------------------------------------------------

    def _detect_rule_conflicts(self):
        """
        Detect if a single rule is bound to multiple invariants
        that imply incompatible enforcement semantics.
        """

        rule_to_invariants = {}

        for inv in self.invariants:
            for rule_id in inv.get("enforces_rules", []):
                rule_to_invariants.setdefault(rule_id, []).append(inv["id"])

        for rule_id, invs in rule_to_invariants.items():
            if len(invs) > 1:
                # Multiple invariants referencing same rule is allowed
                # but only if they support same intents
                intents_sets = [
                    set(self._get_invariant(inv)["supports_intents"])
                    for inv in invs
                ]

                if not self._all_sets_equal(intents_sets):
                    self._fail(
                        f"Rule {rule_id} enforces conflicting invariants {invs}"
                    )

    def _detect_invariant_self_conflicts(self):
        """
        Detect invariant contradictions such as:
        - invariant referencing both deny and require logic rules
        """

        for inv in self.invariants:
            rule_effects = []

            for rule_id in inv.get("enforces_rules", []):
                rule = self.rules.get(rule_id)
                if rule:
                    rule_effects.append(rule.get("effect"))

            if "deny" in rule_effects and "require" in rule_effects:
                self._fail(
                    f"Invariant {inv['id']} mixes deny and require rule effects"
                )

    def _detect_axiom_conflicts(self):
        """
        Detect if invariants derive from incompatible axioms.
        """

        axiom_usage = {}

        for inv in self.invariants:
            for axiom_id in inv.get("derives_from_axioms", []):
                axiom_usage.setdefault(axiom_id, []).append(inv["id"])

        # For now, detect impossible case:
        # If invariant derives from axiom not defined as immutable
        for axiom_id, invs in axiom_usage.items():
            axiom = self._get_axiom(axiom_id)
            if axiom and not axiom.get("immutable", False):
                self._fail(
                    f"Invariant derives from non-immutable axiom {axiom_id}"
                )

    # --------------------------------------------------

    def _get_invariant(self, inv_id):
        for inv in self.invariants:
            if inv["id"] == inv_id:
                return inv
        return None

    def _get_axiom(self, axiom_id):
        for ax in self.axioms:
            if ax["id"] == axiom_id:
                return ax
        return None

    def _all_sets_equal(self, sets):
        return all(s == sets[0] for s in sets)

    def _fail(self, message):
        print(f"❌ Semantic conflict detected: {message}")
        exit(1)


if __name__ == "__main__":
    SemanticConflictValidator().validate()
