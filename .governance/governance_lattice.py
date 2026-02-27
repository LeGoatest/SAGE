import os
from pathlib import Path

def get_sage_root() -> Path:
    """
    Determines the SAGE root directory.
    Priority:
    1. SAGE_ROOT environment variable.
    2. .sage/ directory if it exists in the current working directory.
    3. Current working directory.
    """
    env_root = os.environ.get("SAGE_ROOT")
    if env_root:
        return Path(env_root).resolve()

    dot_sage = Path(".sage")
    if dot_sage.exists() and dot_sage.is_dir():
        return dot_sage.resolve()

    return Path.cwd().resolve()
