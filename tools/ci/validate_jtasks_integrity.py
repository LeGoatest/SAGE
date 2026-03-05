import sys
import yaml
from pathlib import Path

def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    current_task_path = root / ".jtasks/current_task.yaml"

    if not current_task_path.exists():
        print("OK: No current_task.yaml; skipping jtasks integrity validation.")
        sys.exit(0)

    try:
        with open(current_task_path, "r") as f:
            current = yaml.safe_load(f)
    except Exception as e:
        die(f"FAIL: Could not parse current_task.yaml: {e}")

    # 2. Parse fields
    task_id = current.get("task_id")
    iso_run = current.get("iso_run")
    spec_path_str = current.get("spec_path")
    state_path_str = current.get("state_path")

    if not all([task_id, iso_run, spec_path_str, state_path_str]):
        die("FAIL: current_task.yaml missing required fields.")

    run_dir = root / ".jtasks" / iso_run
    spec_path = root / spec_path_str
    state_path = root / state_path_str

    # 3. Validate directories
    if not run_dir.exists(): die(f"FAIL: ISO run directory {run_dir} does not exist.")
    if not (run_dir / "specs").exists(): die(f"FAIL: {run_dir}/specs/ does not exist.")
    if not (run_dir / "runtime").exists(): die(f"FAIL: {run_dir}/runtime/ does not exist.")
    if not (run_dir / "runtime/state").exists(): die(f"FAIL: {run_dir}/runtime/state/ does not exist.")

    # 4. Validate spec files
    if not (spec_path / "requirements.yaml").exists(): die(f"FAIL: {spec_path}/requirements.yaml missing.")
    if not (spec_path / "plan.yaml").exists(): die(f"FAIL: {spec_path}/plan.yaml missing.")

    # 5. Validate runtime manifest
    manifest_path = run_dir / "runtime/context_manifest.yaml"
    if not manifest_path.exists(): die(f"FAIL: {manifest_path} missing.")

    # 6. Validate manifest fields
    try:
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        die(f"FAIL: Could not parse context_manifest.yaml: {e}")

    if not manifest.get("version"): die("FAIL: manifest missing version")
    if manifest.get("iso_run") != iso_run: die("FAIL: manifest iso_run mismatch")
    if manifest.get("active_task_id") != task_id: die("FAIL: manifest task_id mismatch")
    if "context_loaded" not in manifest or "task_files" not in manifest["context_loaded"]:
        die("FAIL: manifest missing context_loaded.task_files")
    if not manifest.get("timestamp"): die("FAIL: manifest missing timestamp")

    # 7. Validate required injected files (in context_loaded.task_files)
    task_files = manifest["context_loaded"]["task_files"]
    required_in_manifest = [str(state_path), str(spec_path / "plan.yaml"), str(spec_path / "requirements.yaml")]
    for rf in required_in_manifest:
        if rf not in task_files:
            die(f"FAIL: Required file {rf} not listed in context_manifest.yaml")

    # 8. Ensure GAP_REPORT.md is NOT present
    for tf in task_files:
        if "GAP_REPORT.md" in tf:
            die("FAIL: GAP_REPORT.md must never be injected into agent context.")

    # 9. Validate runtime state YAML
    try:
        with open(state_path, "r") as f:
            state = yaml.safe_load(f)
    except Exception as e:
        die(f"FAIL: Could not parse state file {state_path}: {e}")

    required_state_fields = ["task_id", "status", "current_step_id", "progress", "working_set", "decisions", "last_update"]
    for field in required_state_fields:
        if field not in state:
            die(f"FAIL: state.yaml missing required field: {field}")

    print("OK: JTASKS integrity validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
