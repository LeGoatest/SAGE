class ContextPruner:
    def __init__(self, token_limit: int = 4000):
        self.token_limit = token_limit

    def prune_context(self, context: dict) -> dict:
        files = context.get("files", [])

        # Simple token estimation: 1 token approx 4 chars
        current_length = sum(len(f["content"]) for f in files)
        if current_length / 4 <= self.token_limit:
            return context

        # Priority calculation
        def get_priority(file_id: str) -> int:
            if "architecture_rules" in file_id: return 1
            if "task_groups" in file_id: return 2
            if ":rules" in file_id or "canon/rules" in file_id: return 3
            if "skills" in file_id: return 4
            return 5

        # Sort files by priority (lowest number first)
        sorted_files = sorted(files, key=lambda x: get_priority(x["id"]))

        pruned_files = []
        accumulated_chars = 0
        limit_chars = self.token_limit * 4

        # Keep critical files regardless of limit if they fit
        critical_threshold = 3 # rules and above

        for f in sorted_files:
            file_len = len(f["content"])
            priority = get_priority(f["id"])

            if priority <= critical_threshold:
                # Critical files are always included if they fit in the total limit
                if accumulated_chars + file_len <= limit_chars:
                    pruned_files.append(f)
                    accumulated_chars += file_len
            else:
                # Non-critical files are included only if there's remaining space
                if accumulated_chars + file_len <= limit_chars:
                    pruned_files.append(f)
                    accumulated_chars += file_len

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
