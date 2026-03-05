from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple


RE_JTASK_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$")  # ISO-ish folder used by SAGE


def find_latest_jtask(root: Path) -> Optional[Path]:
    jtasks = root / ".jtasks"
    if not jtasks.exists() or not jtasks.is_dir():
        return None
    candidates = [p for p in jtasks.iterdir() if p.is_dir() and RE_JTASK_DIR.match(p.name)]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.name)
    return candidates[-1]


def parse_tasks_modified_files(tasks_md: Path) -> list[Path]:
    """
    Best-effort parse of tasks.md to find file paths under "Files Modified:" sections.
    We treat any listed file path that exists in repo as a brownfield modification indicator.
    """
    text = tasks_md.read_text(encoding="utf-8", errors="replace")
    files: list[Path] = []

    # Capture indented bullets after "Files Modified:" until a blank line or next header-ish line.
    # This is intentionally forgiving.
    pattern = re.compile(r"(?im)^\s*Files Modified:\s*\n((?:\s*-\s*.+\n)+)")
    for m in pattern.finditer(text):
        block = m.group(1)
        for line in block.splitlines():
            line = line.strip()
            if not line.startswith("-"):
                continue
            raw = line[1:].strip()
            if not raw or raw.upper().startswith("TODO"):
                continue
            files.append(Path(raw))
    return files


def has_blocker_gaps(gap_report_md: Path) -> bool:
    text = gap_report_md.read_text(encoding="utf-8", errors="replace")

    # Any explicit "Risk Level: BLOCKER" is treated as unresolved blocker.
    if re.search(r"(?im)^\s*Risk Level:\s*BLOCKER\s*$", text):
        return True

    # Also catch a compact inline form: "Risk Level: BLOCKER" anywhere on a line.
    if re.search(r"(?im)\bRisk\s*Level\s*:\s*BLOCKER\b", text):
        return True

    return False


def main(argv: list[str]) -> int:
    repo_root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd().resolve()

    if (repo_root / ".jtasks/current_task.yaml").exists():
        print("OK: GAP_REPORT is human-only and excluded from agent context.")
        return 0

    latest = find_latest_jtask(repo_root)
    if latest is None:
        print("OK: No .jtasks/<timestamp>/ found; skipping GAP_REPORT validation.")
        return 0

    # In SAGE v5, we often look at requirements first, but tasks.md is our heuristic for brownfield
    tasks_md = latest / "tasks.md"
    if not tasks_md.exists():
        print(f"OK: {latest.as_posix()} missing tasks.md; skipping GAP_REPORT validation.")
        return 0

    modified = parse_tasks_modified_files(tasks_md)

    # Brownfield heuristic: any listed modified file that already exists in repo.
    brownfield = False
    for rel in modified:
        abs_path = (repo_root / rel).resolve()
        # Ensure it is within repo root and exists.
        try:
            abs_path.relative_to(repo_root)
        except ValueError:
            continue
        if abs_path.exists():
            brownfield = True
            break

    if not brownfield:
        print("OK: No brownfield modifications detected from tasks.md; GAP_REPORT optional.")
        return 0

    gap = latest / "GAP_REPORT.md"
    if not gap.exists():
        print("FAIL: Brownfield modifications detected, but GAP_REPORT.md is missing.")
        print(f"Expected: {gap.as_posix()}")
        return 2

    if has_blocker_gaps(gap):
        print("FAIL: GAP_REPORT.md contains Risk Level: BLOCKER entries.")
        print(f"File: {gap.as_posix()}")
        return 3

    print("OK: Brownfield detected; GAP_REPORT.md present and contains no BLOCKER gaps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
