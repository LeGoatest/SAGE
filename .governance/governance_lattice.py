import yaml
from pathlib import Path

LAYER_ORDER = []

def load_meta():
    meta = yaml.safe_load(Path("canon/canon.meta.yaml").read_text())
    global LAYER_ORDER
    LAYER_ORDER = meta["precedence"]

def layer_priority(layer):
    return LAYER_ORDER.index(layer)

def resolve_conflicts(matching_rules):
    """
    matching_rules: list of dict rules
    Returns final decision: "deny", "require", or "allow"
    """

    # Sort by layer priority
    matching_rules.sort(key=lambda r: layer_priority(r["layer"]))

    # Identity highest precedence
    for rule in matching_rules:
        if rule["effect"] == "deny":
            return "deny"

    requires = [r for r in matching_rules if r["effect"] == "require"]
    if requires:
        return "require"

    return "allow"
