import yaml
from pathlib import Path

# Use absolute path relative to the script's root if possible
# or just assume it's run from the root.
CANON_PATH = Path("canon")
SEMANTIC_PATH = CANON_PATH / "semantic"


class SemanticEngine:

    def __init__(self):
        self.axioms = self._load_yaml("axioms.yaml")["axioms"]
        self.intents = self._load_yaml("intents.yaml")["intents"]
        self.invariants = self._load_yaml("invariants.yaml")["invariants"]
        self.dependencies = self._load_yaml("dependencies.yaml")["dependencies"]
        self.norm_hierarchy = self._load_yaml("norm_hierarchy.yaml")
        self.refusal_logic = self._load_yaml("refusal_logic.yaml")
        self.templates = self._load_yaml("explanation_templates.yaml")["templates"]

        self._index_data()

    def _load_yaml(self, filename):
        path = SEMANTIC_PATH / filename
        if not path.exists():
            # Try alternative path if run from a different context
            alt_path = Path(__file__).parent.parent / "canon" / "semantic" / filename
            if alt_path.exists():
                path = alt_path
        return yaml.safe_load(path.read_text())

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
