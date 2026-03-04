import os
import yaml
import json
import subprocess
import hashlib
import sys
import re
from pathlib import Path
from governance_lattice import get_sage_root

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from engine import SAGEEngine

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"

def load_rules():
    rules = []
    for file in CANON_PATH.joinpath("rules").rglob("*.yaml"):
        data = yaml.safe_load(file.read_text())
        if not data:
            continue
        if isinstance(data, list):
            rules.extend(data)
        else:
            rules.append(data)
    return rules

def compute_canon_hash():
    sha = hashlib.sha256()
    for file in sorted(CANON_PATH.rglob("*")):
        if file.is_file() and file.name != "version_lock.yaml":
            sha.update(file.read_bytes())
    return sha.hexdigest()

def get_changed_files():
    # Attempt to get changed files against main branches
    for target in ["origin/main", "main", "origin/master", "master", "HEAD^"]:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", target],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split("\n")
        except subprocess.CalledProcessError:
            continue
    return []

def find_active_jtask():
    jtasks = Path(".jtasks")
    if not jtasks.exists():
        return None
    candidates = [p for p in jtasks.iterdir() if p.is_dir() and p.name != "_template"]
    if not candidates:
        return None
    candidates.sort(key=lambda x: x.name)
    return candidates[-1]

def match_rule(rule, changed_files):
    if not isinstance(rule, dict):
        return False

    # Handle two formats:
    # 1. Rule with 'match' key (legacy/structured)
    # 2. Rule with 'condition' or 'path_globs' at top level

    match_data = rule.get("match", rule)

    # Path glob matching
    globs = match_data.get("path_globs")
    if globs:
        for file in changed_files:
            if not file: continue
            for glob in globs:
                if Path(file).match(glob.replace("./", "")):
                    # Special check: Governance changes require GOVERNANCE task group
                    # For now, we use the rule ID to check context if available,
                    # but here we just return True to trigger the rule evaluation.
                    return True
        return False

    # Condition matching
    condition = str(match_data.get("condition", ""))
    if not condition:
        return False

    if condition == "CANON_HASH_MISMATCH":
        lock_file = CANON_PATH.joinpath("version_lock.yaml")
        if lock_file.exists():
            expected = yaml.safe_load(lock_file.read_text())["canon_hash"]
            return compute_canon_hash() != expected

    # Structural / Spec checks
    active_jtask = find_active_jtask()

    if "requirements.md AND design.md AND tasks.md exist" in condition:
        if not active_jtask: return True # Missing entire folder is a failure
        return not (all((active_jtask / f).exists() for f in ["requirements.md", "design.md", "tasks.md"]))

    if "requirements.md contains a section header matching" in condition:
        if not active_jtask or not (active_jtask / "requirements.md").exists(): return False
        header_match = re.search(r'"(.+?)"', condition)
        if not header_match: return False
        header = header_match.group(1)
        content = (active_jtask / "requirements.md").read_text()
        return header not in content

    if "Satisfies: REQ-" in condition:
        if not active_jtask or not (active_jtask / "tasks.md").exists(): return False
        content = (active_jtask / "tasks.md").read_text()
        return "Satisfies: REQ-" not in content

    if "Files Modified:" in condition:
        if not active_jtask or not (active_jtask / "tasks.md").exists(): return False
        content = (active_jtask / "tasks.md").read_text()
        return "Files Modified:" not in content

    if "Task modifies existing files OR extends existing components" in condition:
        if not active_jtask or not (active_jtask / "tasks.md").exists(): return False
        text = (active_jtask / "tasks.md").read_text()
        # Look for indented list items after 'Files Modified:'
        pattern = re.compile(r"(?im)^\s*Files Modified:\s*\n((?:\s*-\s*.+\n)+)")
        for m in pattern.finditer(text):
            block = m.group(1)
            for line in block.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    path_str = line[1:].strip()
                    if path_str and not path_str.upper().startswith("TODO"):
                        if Path(path_str).exists():
                            return True
        return False

    if "Risk Level: BLOCKER" in condition:
        if not active_jtask or not (active_jtask / "GAP_REPORT.md").exists(): return False
        content = (active_jtask / "GAP_REPORT.md").read_text()
        return "Risk Level: BLOCKER" in content

    return False

def evaluate():
    # 0. Load Task Group if present
    # In a real environment, this might be passed as an env var SAGE_TASK_GROUP
    current_task_group = os.environ.get("SAGE_TASK_GROUP", "FEATURE")

    engine = SAGEEngine()

    # 1. Canon Boot Validation
    print("Step 1: Canon Boot Validation")
    engine.boot_validate()

    # 2. Invariant Consistency Validation
    print("Step 2: Invariant Consistency Validation")
    engine.invariant_validate()

    # 3. Semantic Conflict Detection
    print("Step 3: Semantic Conflict Detection")
    engine.conflict_validate()

    # 4. Rule Evaluation
    print("Step 4: Rule Evaluation")
    rules = load_rules()
    changed_files = get_changed_files()

    violated_rule_ids = []
    for rule in rules:
        rule_id = rule["id"]

        # Guard: Governance mutations require GOVERNANCE task group
        if rule_id == "SECURITY_PROTECTED_ZONES":
            if current_task_group == "GOVERNANCE":
                continue # Bypass for authorized mutation

        if match_rule(rule, changed_files):
            if rule.get("effect") == "deny" or rule.get("effect") == "require":
                 violated_rule_ids.append(rule_id)

    if violated_rule_ids:
        print("❌ Governance Denied")
        explanation = engine.explain_violation(violated_rule_ids)
        if explanation:
            print("\n--- CONSTITUTIONAL REASONING ---")
            print(explanation)
            print("--------------------------------\n")
        sys.exit(1)

    # 5. Generate Graph (Post-validation)
    print("Step 5: Generate Constitutional Graph")
    engine.generate_graph()

    # 6. Constitutional Derivation Analysis
    print("Step 6: Constitutional Derivation Analysis")
    engine.analyze_derivation()

    print("✅ Governance Passed")

if __name__ == "__main__":
    evaluate()
