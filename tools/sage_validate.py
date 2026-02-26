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

def main() -> None:
    state_schema = load_yaml(ROOT / "src/canon/state-schema-v2.yaml")
    rules_schema = load_yaml(ROOT / "src/canon/rule-schema-v2.governance.yaml")

    # Basic schema sanity
    if state_schema.get("type") != "governance_state_machine":
        die("state-schema-v2.yaml: type must be governance_state_machine")

    states = {s.get("id") for s in state_schema.get("states", [])}
    if not {"normal", "deep", "spec", "exec", "hitl"}.issubset(states):
        die(f"state-schema-v2.yaml: missing required states. Found: {sorted(states)}")

    forbidden = state_schema.get("forbidden_transitions", [])
    if not any(ft.get("from") == "deep" and ft.get("to") == "exec" for ft in forbidden):
        die("state-schema-v2.yaml: must forbid deep -> exec transition")

    # Check rule schema references state ids
    rules = rules_schema.get("rules", [])
    ids = {r.get("id") for r in rules}
    if not {"A11", "A12", "A13"}.issubset(ids):
        die(f"rule-schema-v2.governance.yaml: missing required rules A11/A12/A13. Found: {sorted(ids)}")

    # Validate that A12 references state_id deep
    a12 = next((r for r in rules if r.get("id") == "A12"), None)
    if not a12:
        die("rule-schema-v2.governance.yaml: missing A12")
    mode = a12.get("mode", {})
    if mode.get("state_id") != "deep":
        die("A12.mode.state_id must be 'deep'")

    algo = mode.get("algorithm", {})
    if algo.get("max_passes") != 3:
        die("A12.mode.algorithm.max_passes must be 3")

    print("SAGE-VALIDATE: OK")

if __name__ == "__main__":
    main()
