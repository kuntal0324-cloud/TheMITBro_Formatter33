from dataclasses import dataclass
from pathlib import Path
@dataclass
class OCRResult:
 text:str
 confidence:float

def extract_text(path):
 p=Path(path)
 return OCRResult(p.read_text() if p.suffix in [".txt",".md"] else "",0.95)
