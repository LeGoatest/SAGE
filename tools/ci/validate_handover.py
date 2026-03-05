from __future__ import annotations
import sys
import re
from pathlib import Path

RE_JTASK_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$")

def find_latest_jtask(root: Path):
    jtasks = root / ".jtasks"
    if not jtasks.exists():
        return None
    candidates = [p for p in jtasks.iterdir() if p.is_dir() and RE_JTASK_DIR.match(p.name)]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.name)
    return candidates[-1]

def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd().resolve()

    if (root / ".jtasks/current_task.yaml").exists():
        print("OK: HANDOVER deprecated; skipping legacy validator.")
        return 0

    latest = find_latest_jtask(root)

    if latest is None:
        print("OK: No active .jtasks folder.")
        return 0

    tasks_md = latest / "tasks.md"
    handover_md = latest / "HANDOVER.md"

    if not tasks_md.exists():
        print("OK: No tasks.md; nothing to validate.")
        return 0

    text = tasks_md.read_text(encoding="utf-8", errors="replace")

    incomplete = "TASK-" in text and "Completion Criteria" not in text

    if incomplete and not handover_md.exists():
        print("FAIL: Incomplete execution detected but HANDOVER.md missing.")
        return 2

    if handover_md.exists():
        htext = handover_md.read_text(encoding="utf-8", errors="replace")
        if "Active canon ref" not in htext:
            print("FAIL: HANDOVER.md missing canon reference.")
            return 3

    print("OK: HANDOVER validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
