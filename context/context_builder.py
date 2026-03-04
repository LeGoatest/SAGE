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

        return {
            "resolved_nodes": resolved_ids,
            "files": files,
            "missing": missing
        }

if __name__ == "__main__":
    builder = ContextBuilder()
    context = builder.build_context(["agent:jules"])
    print(f"Resolved nodes: {context['resolved_nodes']}")
    print(f"Files loaded: {len(context['files'])}")
    print(f"Missing files: {context['missing']}")
