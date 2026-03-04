from __future__ import annotations

import sys
import os
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception as e:
    print("SAGE-VALIDATE: PyYAML is required (pip install pyyaml).", file=sys.stderr)
    raise

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

# Add .governance to path so we can import semantic_engine
sys.path.append(str(ROOT / ".governance"))

try:
    from semantic_engine import SemanticEngine
except ImportError:
    # If not present yet, we'll handle it gracefully for bootstrap
    SemanticEngine = None

def die(msg: str) -> None:
    print(f"SAGE-VALIDATE: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load_yaml(path: Path) -> dict:
    if not path.exists():
        die(f"Missing YAML: {path.as_posix()}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def validate_semantic_layer() -> None:
    if not SemanticEngine:
        print("SAGE-VALIDATE: SemanticEngine not found, skipping deep validation.")
        return

    try:
        engine = SemanticEngine()
    except Exception as e:
        die(f"SemanticEngine initialization failed: {e}")

    errors = []

    # 1. Structural Integrity: Ensure all cross-references exist
    for inv in engine.invariants:
        inv_id = inv.get("id")
        for intent_id in inv.get("supports_intents", []):
            if intent_id not in engine.intent_index:
                errors.append(f"Invariant {inv_id} references unknown intent {intent_id}")
        for axiom_id in inv.get("derives_from_axioms", []):
            if axiom_id not in engine.axiom_index:
                errors.append(f"Invariant {inv_id} references unknown axiom {axiom_id}")

    # 2. Dependencies consistency
    a2i = engine.dependencies.get("axioms_to_intents", {})
    for axiom_id, intent_list in a2i.items():
        if axiom_id not in engine.axiom_index:
            errors.append(f"dependencies.yaml: unknown axiom {axiom_id} in axioms_to_intents")
        for intent_id in intent_list:
            if intent_id not in engine.intent_index:
                errors.append(f"dependencies.yaml: unknown intent {intent_id} for axiom {axiom_id}")

    i2v = engine.dependencies.get("intents_to_invariants", {})
    for intent_id, inv_list in i2v.items():
        if intent_id not in engine.intent_index:
            errors.append(f"dependencies.yaml: unknown intent {intent_id} in intents_to_invariants")
        for inv_id in inv_list:
            if inv_id not in engine.invariant_index:
                errors.append(f"dependencies.yaml: unknown invariant {inv_id} for intent {intent_id}")

    # 3. Orphan Detection
    referenced_axioms = set()
    for intent_list in a2i.values():
        pass # just checking mapping
    for inv in engine.invariants:
        for axiom_id in inv.get("derives_from_axioms", []):
            referenced_axioms.add(axiom_id)

    for axiom in engine.axioms:
        if axiom["id"] not in referenced_axioms and axiom["id"] not in a2i:
             print(f"SAGE-VALIDATE: Warning: Orphan axiom {axiom['id']} detected.")

    referenced_intents = set()
    for inv in engine.invariants:
        for intent_id in inv.get("supports_intents", []):
            referenced_intents.add(intent_id)

    for intent in engine.intents:
        if intent["id"] not in referenced_intents:
            print(f"SAGE-VALIDATE: Warning: Orphan intent {intent['id']} detected.")

    # 4. Circular Dependency Check (Axiom -> Intent -> Invariant)
    # This is naturally a DAG in SAGE, but we should ensure no weird loops in dependencies.yaml
    # (Omitted for brevity unless complex graphs are expected)

    if errors:
        for err in errors:
            print(f"SAGE-VALIDATE: Error: {err}", file=sys.stderr)
        die("Semantic Layer validation failed.")

    print("SAGE-VALIDATE: Semantic Layer OK")

def main() -> None:
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

    # Demonstration of the reasoning engine if a rule is passed as arg
    if len(sys.argv) > 2:
        violated_rule = sys.argv[2]
        if SemanticEngine:
            engine = SemanticEngine()
            explanation = engine.evaluate_violation([violated_rule])
            if explanation:
                print("\n--- CONSTITUTIONAL REASONING ---")
                print(explanation)
                print("--------------------------------\n")

    print("SAGE-VALIDATE: OK")

if __name__ == "__main__":
    main()
