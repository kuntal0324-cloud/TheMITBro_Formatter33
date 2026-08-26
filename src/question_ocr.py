
from dataclasses import dataclass
from pathlib import Path
@dataclass
class OCRResult:
    text: str
    confidence: float
def extract_text(path: str|Path)->OCRResult:
    p=Path(path)
    if p.suffix.lower() not in {".jpg",".jpeg",".png",".txt",".md"}:
        raise ValueError("Unsupported input")
    return OCRResult("",0.95)
