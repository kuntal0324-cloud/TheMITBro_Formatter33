
import json
from pathlib import Path
def load_catalog(root):
    p=Path(root)/"catalog.json"
    return json.loads(p.read_text()) if p.exists() else {"questions":[]}
