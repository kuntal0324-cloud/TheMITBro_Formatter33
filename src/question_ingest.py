from __future__ import annotations

import hashlib
import shutil
import uuid
from pathlib import Path

from .question_bank_schema import QuestionRecord
from .question_classifier import classify_question


SUPPORTED = {".txt", ".md", ".jpg", ".jpeg"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _ocr_image(path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "JPG/JPEG ingestion requires optional OCR dependencies: "
            "Pillow and pytesseract."
        ) from exc

    try:
        return pytesseract.image_to_string(Image.open(path))
    except Exception as exc:
        raise RuntimeError(f"OCR failed for {path.name}: {exc}") from exc


def extract_text(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"Unsupported question source: {path.suffix}")

    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8"), "text"

    return _ocr_image(path), "image"


def ingest(path: str | Path, *, exam_hint: str | None = None) -> QuestionRecord:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)

    text, source_type = extract_text(source)
    text = text.strip()
    if not text:
        raise ValueError("Question source contains no readable text.")

    classification = classify_question(text, exam_hint=exam_hint)

    return QuestionRecord(
        id="QB-" + uuid.uuid4().hex[:12].upper(),
        schema_version="1.0",
        source_type=source_type,
        source_sha256=sha256_file(source),
        source_name=source.name,
        text=text,
        classification=classification,
    )


def copy_original_image(source: Path, record: QuestionRecord, assets_dir: Path) -> str | None:
    if record.source_type != "image":
        return None
    assets_dir.mkdir(parents=True, exist_ok=True)
    target = assets_dir / f"{record.id}{source.suffix.lower()}"
    shutil.copy2(source, target)
    return str(target)
