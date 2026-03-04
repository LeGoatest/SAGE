import os
import re
import yaml
import sys
from governance_lattice import get_sage_root

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

def load_yaml_rules(filepath):
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return []

    if not data:
        return []

    rules = data if isinstance(data, list) else [data]
    result = []
    for r in rules:
        if isinstance(r, dict) and r.get('type', 'rule') == 'rule' and 'id' in r:
            # Adapt YAML rule to sagrule-like format for validator
            # YAML rules have different fields (e.g. 'match', 'effect')
            # The compiler's validate_rule expects sagrule fields.
            # We'll just pass them through for uniqueness check for now.
            r['_file'] = filepath
            result.append(r)
    return result

def validate_rule(rule):
    # Only validate rules extracted from MD (sagrules)
    if rule['_file'].endswith('.yaml'):
        return True # YAML rules have their own schema

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

    # Statement check only makes sense for sagrules
    statements = {}
    for rule in rules:
        if 'statement' not in rule or 'operator' not in rule:
            continue

        stmt = str(rule['statement']).strip()
        ctx = rule.get('context', 'all')
        key = (stmt, ctx)
        if key in statements:
            if rule['operator'] != statements[key]['operator']:
                print(f"Contradiction: Rule {rule['id']} conflicts with {statements[key]['id']} on same statement in context {ctx}.")
                return False
        statements[key] = rule
    return True

def main():
    # Determine SAGE root for injection awareness
    sage_root = get_sage_root()

    # Prefer canon/ over ..docs/
    search_dirs = [
        sage_root / 'canon',
        sage_root / 'Jules',
        sage_root / '.docs'
    ]
    all_rules = []
    seen_ids = set()

    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for root, _, files in os.walk(sdir):
            for file in files:
                filepath = os.path.join(root, file)
                if file.endswith('.md'):
                    rules = extract_sagrules(filepath)
                    for r in rules:
                        if r['id'] not in seen_ids:
                            all_rules.append(r)
                            seen_ids.add(r['id'])
                elif file.endswith('.yaml') and 'semantic' not in root:
                    rules = load_yaml_rules(filepath)
                    for r in rules:
                        if r['id'] not in seen_ids:
                            all_rules.append(r)
                            seen_ids.add(r['id'])

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
        print(f"--- SAGE Canon Compiled ---")
        for rule in all_rules:
            op = rule.get('operator', rule.get('effect', 'rule')).upper()
            stmt = rule.get('statement', rule.get('message', ''))
            print(f"[{rule['id']}] {op}: {str(stmt)[:50]}...")
        print(f"---------------------------")
        print(f"SUCCESS: {len(all_rules)} rules verified.")

if __name__ == "__main__":
    main()
