import yaml
from pathlib import Path

class ContextBuilder:
    def __init__(self, graph_path: str = "canon/graph.yaml"):
        self.graph_path = Path(graph_path)
        self.graph = self._load_graph()
        self.nodes = {node["id"]: node for node in self.graph.get("nodes", [])}

    def _load_graph(self) -> dict:
        if not self.graph_path.exists():
            return {"nodes": []}
        with open(self.graph_path, "r") as f:
            return yaml.safe_load(f)

    def resolve_dependencies(self, seed_nodes: list[str]) -> list[str]:
        resolved = []
        visited = set()

        def visit(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            node = self.nodes.get(node_id)
            if not node:
                return
            for dep in node.get("depends_on", []):
                visit(dep)
            resolved.append(node_id)

        for seed in seed_nodes:
            visit(seed)
        return resolved

    def build_context(self, seed_nodes: list[str] = None) -> dict:
        if seed_nodes is None:
            seed_nodes = [self.graph.get("root", "canon:constitution")]
        resolved_ids = self.resolve_dependencies(seed_nodes)
        files = []
        missing = []

        # 1. Resolve canon graph resolution
        for node_id in resolved_ids:
            node = self.nodes[node_id]
            machine_path = Path(node["machine"])
            if machine_path.exists():
                with open(machine_path, "r") as f:
                    files.append({
                        "id": node_id,
                        "path": node["machine"],
                        "content": f.read()
                    })
            else:
                missing.append(node["machine"])

            if "human" in node:
                human_path = Path(node["human"])
                if human_path.exists():
                    with open(human_path, "r") as f:
                        files.append({
                            "id": f"{node_id}:human",
                            "path": node["human"],
                            "content": f.read()
                        })
                else:
                    missing.append(node["human"])

        # 2. Add skills registry (in this specific assembly order)
        # Note: skills metadata loading is handled by skill_loader but for context bundle,
        # we ensure files are injected here or by the tool calling build_context.

        # 3. Active task context (.jtasks)
        task_files, task_missing = self._load_active_task_context()
        files.extend(task_files)
        missing.extend(task_missing)

        return {
            "resolved_nodes": resolved_ids,
            "files": files,
            "missing": missing
        }

    def _load_active_task_context(self) -> tuple[list[dict], list[str]]:
        current_task_path = Path(".jtasks/current_task.yaml")
        if not current_task_path.exists():
            return [], []

        try:
            with open(current_task_path, "r") as f:
                current = yaml.safe_load(f)

            if not current or not current.get("task_id"):
                return [], []

            spec_path = Path(current["spec_path"])
            state_path = Path(current["state_path"])

            if not spec_path.exists() or not spec_path.is_dir():
                return [], [str(spec_path)]
            if not state_path.exists():
                return [], [str(state_path)]

            req_file = spec_path / "requirements.yaml"
            plan_file = spec_path / "plan.yaml"

            if not req_file.exists() or not plan_file.exists():
                raise ValueError("Invalid active task: missing required spec/state files")

            files_to_inject = []

            # Order: state, plan, requirements, design
            paths = [
                (state_path, "task:state"),
                (plan_file, "task:plan"),
                (req_file, "task:requirements")
            ]

            design_file = spec_path / "design.yaml"
            if design_file.exists():
                paths.append((design_file, "task:design"))

            for path, node_id in paths:
                with open(path, "r") as f:
                    files_to_inject.append({
                        "id": node_id,
                        "path": str(path),
                        "content": f.read()
                    })

            return files_to_inject, []
        except Exception as e:
            if "missing required spec/state files" in str(e):
                raise
            return [], []

if __name__ == "__main__":
    builder = ContextBuilder()
    context = builder.build_context(["agent:jules"])
    print(f"Resolved nodes: {context['resolved_nodes']}")
    print(f"Files loaded: {len(context['files'])}")
    print(f"Missing files: {context['missing']}")
