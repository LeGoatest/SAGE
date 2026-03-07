import sys
from pathlib import Path

# Add project root to sys.path to import from context/
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from context.context_builder import ContextBuilder
from context.context_pruner import ContextPruner

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/context_resolve.py <node_id> [token_limit]")
        sys.exit(1)

    seed_node = sys.argv[1]
    token_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 4000

    builder = ContextBuilder(str(ROOT / "canon/graph.yaml"))
    context = builder.build_context([seed_node])

    if context["missing"]:
        print(f"Warning: Missing files: {context['missing']}", file=sys.stderr)

    pruner = ContextPruner(token_limit=token_limit)
    pruned_context = pruner.prune_context(context)

    print(f"--- RESOLVED CONTEXT FOR {seed_node} ---")
    print(f"Nodes: {', '.join(pruned_context['resolved_nodes'])}")
    print(f"Token Limit: {token_limit}")
    if pruned_context.get("pruned"):
        print("Status: PRUNED")
    else:
        print("Status: FULL")
    print("--------------------------------------")

    for f in pruned_context["files"]:
        print(f"\nFILE: {f['path']}")
        print("-" * len(f['path']))
        # Print first 100 chars for brevity in CLI output
        content = f['content']
        if len(content) > 100:
            print(content[:100] + "...")
        else:
            print(content)

if __name__ == "__main__":
    main()
