import yaml
import json
import subprocess
import hashlib
from pathlib import Path
from lattice import load_meta, resolve_conflicts

load_meta()

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
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().split("\n")


def match_rule(rule, changed_files):
    match = rule.get("match", {})

    # Path glob matching
    globs = match.get("path_globs")
    if globs:
        for file in changed_files:
            for glob in globs:
                if Path(file).match(glob.replace("./", "")):
                    return True
        return False

    # Condition matching
    condition = match.get("condition")
    if condition == "CANON_HASH_MISMATCH":
        expected = yaml.safe_load(
            CANON_PATH.joinpath("version_lock.yaml").read_text()
        )["canon_hash"]
        return compute_canon_hash() != expected

    return True


def evaluate():
    rules = load_rules()
    changed_files = get_changed_files()

    matching_rules = []
    for rule in rules:
        if match_rule(rule, changed_files):
            matching_rules.append(rule)

    decision = resolve_conflicts(matching_rules)

    if decision == "deny":
        print("❌ Governance Denied")
        exit(1)

    if decision == "require":
        print("⚠ Governance Requirements Not Met")
        exit(1)

    print("✅ Governance Passed")


if __name__ == "__main__":
    evaluate()
