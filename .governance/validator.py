import yaml
import json
import subprocess
import hashlib
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from boot_validator import BootValidator
from invariant_validator import InvariantValidator
from semantic_engine import SemanticEngine

CANON_PATH = Path("canon")

def load_rules():
    rules = []
    for file in CANON_PATH.joinpath("rules").rglob("*.yaml"):
        rules.append(yaml.safe_load(file.read_text()))
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

def match_rule(rule, changed_files):
    match = rule.get("match", {})

    # Path glob matching
    globs = match.get("path_globs")
    if globs:
        for file in changed_files:
            if not file: continue
            for glob in globs:
                if Path(file).match(glob.replace("./", "")):
                    return True
        return False

    # Condition matching
    condition = match.get("condition")
    if condition == "CANON_HASH_MISMATCH":
        lock_file = CANON_PATH.joinpath("identity/version_lock.yaml")
        if not lock_file.exists():
            # Old path?
            lock_file = CANON_PATH.joinpath("version_lock.yaml")

        if lock_file.exists():
            expected = yaml.safe_load(lock_file.read_text())["canon_hash"]
            return compute_canon_hash() != expected

    return False

def evaluate():
    # 1. Canon Boot Validation
    print("Step 1: Canon Boot Validation")
    boot_validator = BootValidator()
    boot_validator.validate()

    # 2. Invariant Consistency Validation
    print("Step 2: Invariant Consistency Validation")
    inv_validator = InvariantValidator()
    inv_validator.validate()

    # 3. Rule Evaluation
    print("Step 3: Rule Evaluation")
    rules = load_rules()
    changed_files = get_changed_files()

    violated_rule_ids = []
    for rule in rules:
        if match_rule(rule, changed_files):
            # In this simple version, any match is a violation for demonstration
            # In a real lattice system, resolve_conflicts would decide.
            if rule.get("effect") == "deny":
                 violated_rule_ids.append(rule["id"])

    if violated_rule_ids:
        print("❌ Governance Denied")
        engine = SemanticEngine()
        explanation = engine.evaluate_violation(violated_rule_ids)
        if explanation:
            print("\n--- CONSTITUTIONAL REASONING ---")
            print(explanation)
            print("--------------------------------\n")
        sys.exit(1)

    print("✅ Governance Passed")

if __name__ == "__main__":
    evaluate()
