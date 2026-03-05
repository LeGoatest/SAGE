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
                # Hard exclusion for templates, GAP_REPORT, HANDOVER and specified patterns
                if machine_path.name in ["GAP_REPORT.md", "HANDOVER.md"] or ".jtasks/_template/" in str(machine_path):
                    continue
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
                    if human_path.name in ["GAP_REPORT.md", "HANDOVER.md"] or ".jtasks/_template/" in str(human_path):
                        continue
                    with open(human_path, "r") as f:
                        files.append({
                            "id": f"{node_id}:human",
                            "path": node["human"],
                            "content": f.read()
                        })
                else:
                    missing.append(node["human"])

        # 2. Add skills registry
        # (Implemented by external callers using skill_loader)

        # 3. SAGE_SYSTEM.yaml
        manifest_path = Path("SAGE_SYSTEM.yaml")
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                files.append({
                    "id": "system:manifest",
                    "path": "SAGE_SYSTEM.yaml",
                    "content": f.read()
                })
        else:
            missing.append("SAGE_SYSTEM.yaml")

        # 4. Scheduler and Event Log
        for extra in [".jtasks/scheduler.yaml", ".jtasks/events.log"]:
            extra_path = Path(extra)
            if extra_path.exists():
                with open(extra_path, "r") as f:
                    files.append({
                        "id": f"task:{extra_path.stem}",
                        "path": extra,
                        "content": f.read()
                    })

        # 5. Active task context (.jtasks)
        task_files, task_missing = self._load_active_task_context()
        files.extend(task_files)
        missing.extend(task_missing)

        # 6. Record context loaded event
        self._record_context_loaded_event()

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
                if path.name in ["GAP_REPORT.md", "HANDOVER.md"] or ".jtasks/_template/" in str(path):
                    continue
                with open(path, "r") as f:
                    files_to_inject.append({
                        "id": node_id,
                        "path": str(path),
                        "content": f.read()
                    })

            # 5. Record injected files in context_manifest.yaml
            self._write_context_manifest(current, files_to_inject)

            return files_to_inject, []
        except Exception as e:
            if "missing required spec/state files" in str(e):
                raise
            return [], []

    def _record_context_loaded_event(self):
        current_task_path = Path(".jtasks/current_task.yaml")
        if not current_task_path.exists():
            return

        try:
            with open(current_task_path, "r") as f:
                current = yaml.safe_load(f)

            if not current or not current.get("task_id"):
                return

            import json
            import datetime
            event = {
                "time": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
                "event": "context_loaded",
                "task": current["task_id"]
            }

            log_path = Path(".jtasks/events.log")
            with open(log_path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception:
            pass

    def _write_context_manifest(self, current: dict, files: list[dict]):
        try:
            iso_run = current["iso_run"]
            manifest_path = Path(".jtasks") / iso_run / "runtime" / "context_manifest.yaml"

            # Ensure directory exists
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            import datetime
            manifest = {
                "version": 1,
                "iso_run": iso_run,
                "active_task_id": current["task_id"],
                "context_loaded": {
                    "canon_nodes": [], # Placeholder for actual resolved nodes
                    "task_files": [f["path"] for f in files],
                    "repository_files": []
                },
                "hashes": {},
                "agent": {
                    "name": "Jules",
                    "version": "1.0"
                },
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z"
            }

            with open(manifest_path, "w") as f:
                yaml.dump(manifest, f)
        except Exception:
            pass

if __name__ == "__main__":
    builder = ContextBuilder()
    context = builder.build_context(["agent:jules"])
    print(f"Resolved nodes: {context['resolved_nodes']}")
    print(f"Files loaded: {len(context['files'])}")
    print(f"Missing files: {context['missing']}")
