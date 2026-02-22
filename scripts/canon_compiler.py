import os
import re
import yaml
import sys

def extract_sagrules(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return []

    blocks = re.findall(r'```yaml sagrule\n(.*?)\n```', content, re.DOTALL)
    rules = []
    for block in blocks:
        try:
            rule = yaml.safe_load(block)
            if rule:
                rule['_file'] = filepath
                rules.append(rule)
        except yaml.YAMLError as exc:
            print(f"Error in {filepath}: {exc}")
            sys.exit(1)
    return rules

def validate_rule(rule):
    required_fields = ['id', 'statement', 'operator', 'context', 'severity', 'enforcement']
    for field in required_fields:
        if field not in rule:
            print(f"Error: Rule {rule.get('id', 'UNKNOWN')} in {rule['_file']} missing field {field}")
            return False

    valid_operators = ['MUST', 'MUST_NOT', 'SHALL', 'SHALL_NOT']
    if rule['operator'] not in valid_operators:
        print(f"Error: Rule {rule['id']} has invalid operator {rule['operator']}")
        return False

    return True

def check_contradictions(rules):
    ids = {}
    for rule in rules:
        rid = rule['id']
        if rid in ids:
            print(f"Contradiction: Duplicate Rule ID {rid} found in {rule['_file']} and {ids[rid]['_file']}")
            return False
        ids[rid] = rule

    statements = {}
    for rule in rules:
        stmt = rule['statement'].strip()
        ctx = rule['context']
        key = (stmt, ctx)
        if key in statements:
            if rule['operator'] != statements[key]['operator']:
                print(f"Contradiction: Rule {rule['id']} conflicts with {statements[key]['id']} on same statement in context {ctx}.")
                return False
        statements[key] = rule
    return True

def main():
    search_dirs = ['src', 'Jules']
    all_rules = []

    for sdir in search_dirs:
        for root, _, files in os.walk(sdir):
            for file in files:
                if file.endswith('.md'):
                    all_rules.extend(extract_sagrules(os.path.join(root, file)))

    if not all_rules:
        print("No rules found to compile.")
        return

    success = True
    for rule in all_rules:
        if not validate_rule(rule):
            success = False

    if success:
        if not check_contradictions(all_rules):
            success = False

    if not success:
        print("Canon compilation FAILED.")
        sys.exit(1)
    else:
        print(f"--- SAGT Canon Compiled ---")
        for rule in all_rules:
            print(f"[{rule['id']}] {rule['operator']}: {rule['statement'][:50]}...")
        print(f"---------------------------")
        print(f"SUCCESS: {len(all_rules)} rules verified.")

if __name__ == "__main__":
    main()
