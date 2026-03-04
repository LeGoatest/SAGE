class ContextPruner:
    def __init__(self, token_limit: int = 4000):
        self.token_limit = token_limit

    def prune_context(self, context: dict) -> dict:
        files = context.get("files", [])

        # Simple token estimation: 1 token approx 4 chars
        current_length = sum(len(f["content"]) for f in files)
        if current_length / 4 <= self.token_limit:
            return context

        # Pruning strategy: Keep foundation nodes, remove others from bottom up
        # We assume build_context returned them in dependency order (foundation first)
        pruned_files = []
        accumulated_chars = 0
        limit_chars = self.token_limit * 4

        for f in files:
            file_len = len(f["content"])
            if accumulated_chars + file_len <= limit_chars:
                pruned_files.append(f)
                accumulated_chars += file_len
            else:
                # If it's a foundation node, we might want to keep it even if it exceeds limit?
                # For now, strictly enforce limit.
                break

        return {
            "resolved_nodes": [f["id"] for f in pruned_files],
            "files": pruned_files,
            "missing": context.get("missing", []),
            "pruned": True
        }

if __name__ == "__main__":
    pruner = ContextPruner(token_limit=100)
    test_context = {
        "files": [
            {"id": "a", "content": "foundation rule " * 10},
            {"id": "b", "content": "extra info " * 50}
        ]
    }
    pruned = pruner.prune_context(test_context)
    print(f"Original files: {len(test_context['files'])}")
    print(f"Pruned files: {len(pruned['files'])}")
