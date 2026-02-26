from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception as e:
    print("SAGE-VALIDATE: PyYAML is required (pip install pyyaml).", file=sys.stderr)
    raise

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

def die(msg: str) -> None:
    print(f"SAGE-VALIDATE: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load_yaml(path: Path) -> dict:
    if not path.exists():
        die(f"Missing YAML: {path.as_posix()}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def validate_semantic_layer() -> None:
    axioms_data = load_yaml(ROOT / "canon/semantic/axioms.yaml")
    axioms = axioms_data.get("axioms", [])
    intents_data = load_yaml(ROOT / "canon/semantic/intents.yaml")
    intents = intents_data.get("intents", [])
    invariants_data = load_yaml(ROOT / "canon/semantic/invariants.yaml")
    invariants = invariants_data.get("invariants", [])
    dependencies_data = load_yaml(ROOT / "canon/semantic/dependencies.yaml")
    dependencies = dependencies_data.get("dependencies", {})

    axiom_ids = {a.get("id") for a in axioms}
    intent_ids = {i.get("id") for i in intents}
    inv_ids = {inv.get("id") for inv in invariants}

    for inv in invariants:
        inv_id = inv.get("id")
        for intent_id in inv.get("supports_intents", []):
            if intent_id not in intent_ids:
                die(f"Invariant {inv_id} references unknown intent {intent_id}")
        for axiom_id in inv.get("derives_from_axioms", []):
            if axiom_id not in axiom_ids:
                die(f"Invariant {inv_id} references unknown axiom {axiom_id}")

    # Validate dependencies
    a2i = dependencies.get("axioms_to_intents", {})
    for axiom_id, intent_list in a2i.items():
        if axiom_id not in axiom_ids:
            die(f"dependencies.yaml: unknown axiom {axiom_id} in axioms_to_intents")
        for intent_id in intent_list:
            if intent_id not in intent_ids:
                die(f"dependencies.yaml: unknown intent {intent_id} for axiom {axiom_id}")

    i2v = dependencies.get("intents_to_invariants", {})
    for intent_id, inv_list in i2v.items():
        if intent_id not in intent_ids:
            die(f"dependencies.yaml: unknown intent {intent_id} in intents_to_invariants")
        for inv_id in inv_list:
            if inv_id not in inv_ids:
                die(f"dependencies.yaml: unknown invariant {inv_id} for intent {intent_id}")

    print("SAGE-VALIDATE: Semantic Layer OK")

def main() -> None:
    # Use .docs/canon/ instead of src/canon/
    state_schema = load_yaml(ROOT / ".docs/canon/state-schema-v2.yaml")
    rules_schema = load_yaml(ROOT / ".docs/canon/rule-schema-v2.governance.yaml")

    # Basic schema sanity
    if state_schema.get("type") != "governance_state_machine":
        die(".docs/canon/state-schema-v2.yaml: type must be governance_state_machine")

    states = {s.get("id") for s in state_schema.get("states", [])}
    if not {"normal", "deep", "spec", "exec", "hitl"}.issubset(states):
        die(f".docs/canon/state-schema-v2.yaml: missing required states. Found: {sorted(states)}")

    forbidden = state_schema.get("forbidden_transitions", [])
    if not any(ft.get("from") == "deep" and ft.get("to") == "exec" for ft in forbidden):
        die(".docs/canon/state-schema-v2.yaml: must forbid deep -> exec transition")

    # Check rule schema references state ids
    rules = rules_schema.get("rules", [])
    ids = {r.get("id") for r in rules}
    if not {"A11", "A12", "A13"}.issubset(ids):
        die(f".docs/canon/rule-schema-v2.governance.yaml: missing required rules A11/A12/A13. Found: {sorted(ids)}")

    # Validate that A12 references state_id deep
    a12 = next((r for r in rules if r.get("id") == "A12"), None)
    if not a12:
        die(".docs/canon/rule-schema-v2.governance.yaml: missing A12")
    mode = a12.get("mode", {})
    if mode.get("state_id") != "deep":
        die("A12.mode.state_id must be 'deep'")

    algo = mode.get("algorithm", {})
    if algo.get("max_passes") != 3:
        die("A12.mode.algorithm.max_passes must be 3")

    validate_semantic_layer()

    print("SAGE-VALIDATE: OK")

if __name__ == "__main__":
    main()
