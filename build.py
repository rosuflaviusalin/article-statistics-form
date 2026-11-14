#!/usr/bin/env python3
"""Generează index.html din src/template.html, incluzând imaginile din docs/ ca base64.

Rulare:  python3 build.py
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "src" / "template.html"
OUTPUT = ROOT / "index.html"
PREFIX = "WhatsApp Image 2026-11-13 at 13.10.42"

# Ordinea corespunde array-ului ARTICLES din template (__IMG1__ ... __IMG5__).
IMAGES = [
    f"{PREFIX} (1).jpeg",  # 1. Prima pagină JCM – AI at the Bedside of Psychiatry
    f"{PREFIX} (2).jpeg",  # 2. Forest plot – meta-analiză
    f"{PREFIX}.jpeg",      # 3. Corelație FSFI–BESAQ
    f"{PREFIX} (3).jpeg",  # 4. Clustere PCA
    f"{PREFIX} (4).jpeg",  # 5. Tabelul 6 – comparații între clustere
]


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    for i, name in enumerate(IMAGES, 1):
        data = base64.b64encode((ROOT / "docs" / name).read_bytes()).decode()
        html = html.replace(f"__IMG{i}__", f"data:image/jpeg;base64,{data}")
    if "__IMG" in html:
        raise SystemExit("Eroare: au rămas placeholder-e __IMGn__ neînlocuite.")
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"index.html generat ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
