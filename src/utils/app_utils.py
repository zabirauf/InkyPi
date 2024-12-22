import os
from pathlib import Path

def resolve_path(file_path):
    src_path = Path(os.getenv("SRC_DIR"))

    return str(src_path / file_path)

