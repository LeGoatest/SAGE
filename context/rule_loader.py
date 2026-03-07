import yaml
import re
from pathlib import Path

class RuleLoader:
    def __init__(self, canon_dir: str = "canon/"):
        self.canon_dir = Path(canon_dir)
        self.rules = {}

    def load_rules(self) -> dict:
        # Load from YAML files in canon/rules/
        rules_path = self.canon_dir / "rules"
        if rules_path.exists():
            for yaml_file in rules_path.rglob("*.yaml"):
                with open(yaml_file, "r") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        for rule in data:
                            if isinstance(rule, dict) and "id" in rule:
                                self.rules[rule["id"]] = rule
                    elif isinstance(data, dict) and "id" in data:
                        self.rules[data["id"]] = data
                    elif isinstance(data, dict) and "rules" in data:
                        for rule in data["rules"]:
                            if isinstance(rule, dict) and "id" in rule:
                                self.rules[rule["id"]] = rule

        # Load from Markdown sagrule blocks
        for md_file in self.canon_dir.glob("*.md"):
            self._extract_sagrules(md_file)

        return self.rules

    def _extract_sagrules(self, file_path: Path):
        with open(file_path, "r") as f:
            content = f.read()
            # Match ```yaml sagrule ... ```
            matches = re.finditer(r"```yaml sagrule\s*(.*?)\s*```", content, re.DOTALL)
            for match in matches:
                try:
                    rule_data = yaml.safe_load(match.group(1))
                    if rule_data and "id" in rule_data:
                        self.rules[rule_data["id"]] = rule_data
                except yaml.YAMLError:
                    continue

    def get_rule(self, rule_id: str) -> dict:
        return self.rules.get(rule_id)

if __name__ == "__main__":
    loader = RuleLoader()
    rules = loader.load_rules()
    print(f"Loaded {len(rules)} rules.")
    for rid in list(rules.keys())[:5]:
        print(f" - {rid}")
