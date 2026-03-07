from __future__ import annotations

import sys
import os
from pathlib import Path

try:
    import yaml  # type: ignore
    import jsonschema # type: ignore
except Exception as e:
    print("SAGE-VALIDATE: PyYAML and jsonschema are required (pip install pyyaml jsonschema).", file=sys.stderr)
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

def load_json(path: Path) -> dict:
    import json
    if not path.exists():
        die(f"Missing JSON: {path.as_posix()}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

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
    validate_canon_graph()
    validate_skill_registry()
    validate_task_groups()
    validate_jtasks_folders()
    validate_mutation_guard()

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

def validate_canon_graph() -> None:
    graph_path = ROOT / "canon/graph.yaml"
    if not graph_path.exists():
        die("Missing canon/graph.yaml")

    graph = load_yaml(graph_path)
    nodes = graph.get("nodes", [])
    node_ids = {n.get("id") for n in nodes}

    errors = []
    for node in nodes:
        node_id = node.get("id")
        # Check machine path exists
        machine = node.get("machine")
        if not (ROOT / machine).exists():
            errors.append(f"Node {node_id}: Machine path {machine} does not exist.")

        # Check human path exists if defined
        human = node.get("human")
        if human and not (ROOT / human).exists():
            errors.append(f"Node {node_id}: Human path {human} does not exist.")

        # Check dependencies exist
        for dep in node.get("depends_on", []):
            if dep not in node_ids:
                errors.append(f"Node {node_id}: Unknown dependency {dep}")

    if errors:
        for err in errors:
            print(f"SAGE-VALIDATE: Graph Error: {err}", file=sys.stderr)
        die("Canon graph validation failed.")
    print("SAGE-VALIDATE: Canon Graph OK")

def validate_skill_registry() -> None:
    registry_path = ROOT / "skills_registry.yaml"
    if not registry_path.exists():
        die("Missing skills_registry.yaml")

    registry = load_yaml(registry_path)
    skills = registry.get("skills", [])

    errors = []
    for skill_id in skills:
        skill_dir = ROOT / "skills" / skill_id
        if not skill_dir.exists():
            errors.append(f"Skill {skill_id}: Directory skills/{skill_id} does not exist.")
        elif not (skill_dir / "SKILL.md").exists():
            errors.append(f"Skill {skill_id}: Missing SKILL.md in skills/{skill_id}")

    if errors:
        for err in errors:
            print(f"SAGE-VALIDATE: Skill Error: {err}", file=sys.stderr)
        die("Skill registry validation failed.")
    print("SAGE-VALIDATE: Skill Registry OK")

def validate_task_groups() -> None:
    tg_path = ROOT / "canon/task_groups.yaml"
    schema_path = ROOT / "canon/schema/task_groups.schema.json"

    if not tg_path.exists():
        die("Missing canon/task_groups.yaml")
    if not schema_path.exists():
        die("Missing canon/schema/task_groups.schema.json")

    data = load_yaml(tg_path)
    schema = load_json(schema_path)

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        die(f"Task group schema validation failed: {e.message}")

    task_groups = data.get("task_groups", [])
    ids = [tg.get("id") for tg in task_groups]
    if len(ids) != len(set(ids)):
        die("Task group ids must be unique")

    print("SAGE-VALIDATE: Task Groups OK")

def validate_jtasks_folders() -> None:
    jtasks_path = ROOT / ".jtasks"
    if not jtasks_path.exists():
        return

    errors = []

    # Load valid task groups for state validation
    tg_path = ROOT / "canon/task_groups.yaml"
    valid_groups = []
    if tg_path.exists():
        tg_data = load_yaml(tg_path)
        valid_groups = [tg["id"] for tg in tg_data.get("task_groups", [])]

    import re
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$")

    for folder in jtasks_path.iterdir():
        if not folder.is_dir() or folder.name.startswith("_"):
            continue

        if not iso_pattern.match(folder.name):
            errors.append(f"Folder {folder.name}: Name must follow ISO-8601 format YYYY-MM-DDTHH-MM-SS")
            continue

        # Validate run folder structure
        for sub in ["specs", "runtime", "runtime/state"]:
            if not (folder / sub).exists():
                errors.append(f"Folder {folder.name}: Missing subdirectory {sub}")

        # Validate specs
        specs_dir = folder / "specs"
        if specs_dir.exists():
            for task_dir in specs_dir.iterdir():
                if not task_dir.is_dir(): continue
                for rf in ["requirements.yaml", "plan.yaml"]:
                    if not (task_dir / rf).exists():
                        errors.append(f"Task {task_dir.name}: Missing {rf}")

        # State validation via current_task.yaml or iteration
        state_dir = folder / "runtime/state"
        if state_dir.exists():
            for state_file in state_dir.glob("*.yaml"):
                state = load_yaml(state_file)
                if "task_id" not in state:
                    errors.append(f"State {state_file.name}: missing task_id")
                if "status" not in state:
                    errors.append(f"State {state_file.name}: missing status")
                if "progress" not in state:
                    errors.append(f"State {state_file.name}: missing progress")

    if errors:
        for err in errors:
            print(f"SAGE-VALIDATE: JTasks Error: {err}", file=sys.stderr)
        die("JTasks validation failed.")
    print("SAGE-VALIDATE: JTasks Folders OK")

def validate_mutation_guard() -> None:
    import subprocess

    try:
        # Get modified files in the current commit or staging area
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        modified_files = result.stdout.splitlines()
        # Also check staged files
        result_staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        modified_files.extend(result_staged.stdout.splitlines())
    except Exception:
        # If not a git repo or other git error, skip mutation guard check
        return

    canon_modified = any(f.startswith("canon/") for f in modified_files)
    if not canon_modified:
        return

    # Use .jtasks/current_task.yaml to determine active task group
    current_task_path = ROOT / ".jtasks/current_task.yaml"
    if not current_task_path.exists():
        die("Canon mutation detected but no active task (.jtasks/current_task.yaml) found.")

    current = load_yaml(current_task_path)
    state_path = ROOT / current.get("state_path", "")

    if not state_path.exists():
        die(f"Canon mutation detected but active state file {state_path} does not exist.")

    state = load_yaml(state_path)
    active_group = state.get("task_group")

    if active_group not in ["architecture", "governance"]:
        die(f"Canon mutation is restricted outside architecture/governance tasks. Active group: {active_group}")

    print("SAGE-VALIDATE: Mutation Guard OK")

if __name__ == "__main__":
    main()
