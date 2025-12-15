# src/services/reader.py
import os
from typing import List

def locate_and_read_logs(root: str, client: str, app_name: str, version: str=None) -> List[str]:
    """
    Walk the root LogSpace and return list of log texts matching client/app/version filters.
    """
    found = []
    client = client.lower()
    app_name = app_name.lower() if app_name else None
    version = version or ""
    for dirpath, dirnames, filenames in os.walk(root):
        path_lower = dirpath.lower()
        if client in path_lower and (not app_name or app_name in path_lower) and version in path_lower:
            # read error/info files
            for fn in filenames:
                if fn.endswith(".error") or fn.endswith(".info"):
                    try:
                        with open(os.path.join(dirpath, fn), "r", encoding="utf-8", errors="ignore") as fh:
                            text = fh.read()
                            if text.strip():
                                found.append(text)
                    except Exception:
                        continue
    return found
