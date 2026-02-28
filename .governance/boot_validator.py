import yaml
import hashlib
import sys
from pathlib import Path
from governance_lattice import get_sage_root

# Determine SAGE root for injection awareness
SAGE_ROOT = get_sage_root()
CANON_PATH = SAGE_ROOT / "canon"
SEMANTIC_PATH = CANON_PATH / "semantic"
RULES_PATH = CANON_PATH / "rules"
SCHEMAS_PATH = CANON_PATH / "schemas"


class BootValidator:

    REQUIRED_CANON_FILES = [
        "canon.meta.yaml",
        "capabilities.yaml",
        "proofs.yaml",
        "task_groups.yaml",
        "conditions.yaml",
        "conflict_policy.yaml",
        "telemetry.yaml",
        "version_lock.yaml",
    ]

    REQUIRED_SEMANTIC_FILES = [
        "axioms.yaml",
        "intents.yaml",
        "invariants.yaml",
        "dependencies.yaml",
        "norm_hierarchy.yaml",
        "refusal_logic.yaml",
        "explanation_templates.yaml",
    ]

    REQUIRED_SCHEMA_FILES = [
        "rule.schema.json",
        "capability.schema.json",
        "proposal.schema.json",
    ]

    def validate(self):
        self._check_required_files()
        self._check_duplicate_ids()
        self._check_canon_hash()
        print("✅ Canon boot self-consistency validation passed.")

    # --------------------------------------------------

    def _check_required_files(self):
        for file in self.REQUIRED_CANON_FILES:
            if not (CANON_PATH / file).exists():
                self._fail(f"Missing required canon file: {file}")

        for file in self.REQUIRED_SEMANTIC_FILES:
            if not (SEMANTIC_PATH / file).exists():
                self._fail(f"Missing required semantic file: {file}")

        for file in self.REQUIRED_SCHEMA_FILES:
            if not (SCHEMAS_PATH / file).exists():
                self._fail(f"Missing required schema file: {file}")

    # --------------------------------------------------

    def _check_duplicate_ids(self):
        rule_ids = []
        in_rules_invariant_ids = []

        for file in RULES_PATH.rglob("*.yaml"):
            data = yaml.safe_load(file.read_text())
            if not data:
                continue

            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict) or "id" not in item:
                    continue

                if item.get("type", "rule") == "rule":
                    rule_ids.append(item["id"])
                elif item.get("type") == "invariant":
                    in_rules_invariant_ids.append(item["id"])

        self._assert_unique(rule_ids, "Duplicate rule IDs detected")

        axioms = yaml.safe_load((SEMANTIC_PATH / "axioms.yaml").read_text())["axioms"]
        self._assert_unique([a["id"] for a in axioms], "Duplicate axiom IDs detected")

        intents = yaml.safe_load((SEMANTIC_PATH / "intents.yaml").read_text())["intents"]
        self._assert_unique([i["id"] for i in intents], "Duplicate intent IDs detected")

        invariants = yaml.safe_load((SEMANTIC_PATH / "invariants.yaml").read_text())["invariants"]
        inv_ids = [inv["id"] for inv in invariants]
        inv_ids.extend(in_rules_invariant_ids)

        self._assert_unique(inv_ids, "Duplicate invariant IDs detected")

    # --------------------------------------------------

    def _check_canon_hash(self):
        lock_file = CANON_PATH / "version_lock.yaml"
        if not lock_file.exists():
            self._fail("Missing version_lock.yaml")

        expected = yaml.safe_load(lock_file.read_text())["canon_hash"]

        sha = hashlib.sha256()

        for file in sorted(CANON_PATH.rglob("*")):
            if file.is_file() and file.name != "version_lock.yaml":
                sha.update(file.read_bytes())

        actual = sha.hexdigest()

        if expected != actual:
            self._fail(f"Canon hash mismatch with version_lock.yaml\nExpected: {expected}\nActual:   {actual}")

    # --------------------------------------------------

    def _assert_unique(self, values, error_msg):
        if len(values) != len(set(values)):
            # Find duplicates
            seen = set()
            dupes = [x for x in values if x in seen or seen.add(x)]
            self._fail(f"{error_msg}: {dupes}")

    def _fail(self, message):
        print(f"❌ Boot validation error: {message}")
        exit(1)


if __name__ == "__main__":
    BootValidator().validate()
