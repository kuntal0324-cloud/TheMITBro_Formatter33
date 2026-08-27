from __future__ import annotations

import json
from pathlib import Path


def load_catalog(root: str | Path) -> dict:
    root = Path(root)
    catalog = root / "catalog.json"

    if not catalog.exists():
        return {"questions": []}

    return json.loads(catalog.read_text(encoding="utf-8"))
