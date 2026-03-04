import sys
import json
import yaml
from pathlib import Path

# Add project root to sys.path to import from context/
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from context.context_builder import ContextBuilder
from context.context_pruner import ContextPruner
from context.skill_loader import SkillLoader

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/build_envelope.py <node_id> [token_limit]")
        sys.exit(1)

    seed_node = sys.argv[1]
    token_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 4000

    builder = ContextBuilder(str(ROOT / "canon/graph.yaml"))
    context = builder.build_context([seed_node])

    pruner = ContextPruner(token_limit=token_limit)
    pruned_context = pruner.prune_context(context)

    # Load task groups from canon
    tg_path = ROOT / "canon/task_groups.yaml"
    task_groups = []
    if tg_path.exists():
        with open(tg_path, "r") as f:
            tg_data = yaml.safe_load(f)
            task_groups = tg_data.get("task_groups", [])

    # Load skills
    skill_loader = SkillLoader(str(ROOT / "skills"), str(ROOT / "skills_registry.yaml"))
    skills = skill_loader.load_skills()

    envelope = {
        "version": 1,
        "resolved_nodes": pruned_context["resolved_nodes"],
        "policy_files": [
            {"id": f["id"], "path": f["path"], "content": f["content"]}
            for f in pruned_context["files"]
        ],
        "skills": skills,
        "task_groups": task_groups,
        "metadata": {
            "seed_node": seed_node,
            "token_limit": token_limit,
            "pruned": pruned_context.get("pruned", False)
        }
    }

    dist_dir = ROOT / "dist"
    dist_dir.mkdir(exist_ok=True)

    output_path = dist_dir / "envelope.json"
    with open(output_path, "w") as f:
        json.dump(envelope, f, indent=2)

    print(f"SAGE: Context envelope built at {output_path}")

if __name__ == "__main__":
    main()
