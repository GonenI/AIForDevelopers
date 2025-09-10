from __future__ import annotations
from typing import Optional
from PIL import Image

try:
    import easyocr
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    easyocr = None

_reader: Optional[easyocr.Reader] = None

def is_ocr_available() -> bool:
    return HAS_OCR


def extract_text(img: Image.Image, lang: str = "en") -> str:
    """Extract text from a PIL Image using easyocr."""
    global _reader
    if not HAS_OCR:
        raise RuntimeError("easyocr is not installed.")
    if _reader is None:
        _reader = easyocr.Reader([lang], gpu=False)
    # Convert PIL Image to numpy array
    import numpy as np
    arr = np.array(img.convert("RGB"))
    results = _reader.readtext(arr, detail=0)
    return "\n".join(results)
