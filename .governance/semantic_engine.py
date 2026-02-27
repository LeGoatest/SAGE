import yaml
from pathlib import Path
from governance_lattice import get_sage_root

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"


class SemanticEngine:

    def __init__(self):
        self.axioms = self._load_semantic("axioms.yaml")["axioms"]
        self.intents = self._load_semantic("intents.yaml")["intents"]
        self.invariants = self._load_semantic("invariants.yaml")["invariants"]
        self.dependencies = self._load_semantic("dependencies.yaml")["dependencies"]
        self.norm_hierarchy = self._load_semantic("norm_hierarchy.yaml")
        self.refusal_logic = self._load_semantic("refusal_logic.yaml")
        self.templates = self._load_semantic("explanation_templates.yaml")["templates"]

        self._load_additional_invariants()
        self._index_data()

    def _load_semantic(self, filename):
        path = SEMANTIC_PATH / filename
        if not path.exists():
            # Try alternative path if run from a different context
            alt_path = Path(__file__).parent.parent / "canon" / "semantic" / filename
            if alt_path.exists():
                path = alt_path
        return yaml.safe_load(path.read_text())

    def _load_additional_invariants(self):
        path = RULES_PATH
        if not path.exists():
            path = Path(__file__).parent.parent / "canon" / "rules"

        for file in path.rglob("*.yaml"):
            data = yaml.safe_load(file.read_text())
            if not data:
                continue

            items = data if isinstance(data, list) else [data]
            for item in items:
                if isinstance(item, dict) and item.get("type") == "invariant":
                    self.invariants.append(item)

    def _index_data(self):
        self.axiom_index = {a["id"]: a for a in self.axioms}
        self.intent_index = {i["id"]: i for i in self.intents}
        self.invariant_index = {inv["id"]: inv for inv in self.invariants}

    # --------------------------------------------------------
    # PUBLIC ENTRY POINT
    # --------------------------------------------------------

    def evaluate_violation(self, violated_rule_ids):
        """
        Given rule IDs that failed,
        derive invariant + intent + axiom context.
        """

        violated_invariants = self._map_rules_to_invariants(violated_rule_ids)

        if not violated_invariants:
            return None

        # Check if invariant derives from axiom
        for inv_id in violated_invariants:
            inv = self.invariant_index[inv_id]

            for axiom_id in inv.get("derives_from_axioms", []):
                if self._axiom_violation(axiom_id):
                    return self._explain_axiom_violation(
                        axiom_id,
                        inv_id,
                        violated_rule_ids[0]
                    )

        # Otherwise explain invariant violation
        return self._explain_invariant_violation(
            violated_invariants[0],
            violated_rule_ids[0]
        )

    # --------------------------------------------------------
    # MAPPING LOGIC
    # --------------------------------------------------------

    def _map_rules_to_invariants(self, violated_rule_ids):
        matches = []

        for inv in self.invariants:
            enforced = inv.get("enforces_rules", [])
            for rule_id in violated_rule_ids:
                if rule_id in enforced:
                    matches.append(inv["id"])

        return matches

    def _axiom_violation(self, axiom_id):
        # Axiom violations occur if invariant derives from immutable axiom
        axiom = self.axiom_index.get(axiom_id)
        return axiom and axiom.get("immutable", False)

    # --------------------------------------------------------
    # EXPLANATION GENERATORS
    # --------------------------------------------------------

    def _explain_invariant_violation(self, invariant_id, rule_id):
        invariant = self.invariant_index[invariant_id]
        intent_id = invariant.get("supports_intents", [None])[0]

        template = self.templates["invariant_violation"]["format"]

        return template.format(
            invariant_id=invariant_id,
            intent_id=intent_id,
            rule_id=rule_id,
            reason_code=rule_id
        )

    def _explain_axiom_violation(self, axiom_id, invariant_id, rule_id):
        template = self.templates["axiom_violation"]["format"]

        return template.format(
            axiom_id=axiom_id,
            reason_code=rule_id
        )
