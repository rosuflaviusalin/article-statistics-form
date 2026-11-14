#!/usr/bin/env python3
"""Generează index.html din src/template.html, incluzând ca base64 imaginile din docs/
și fonturile din src/fonts/ (ca pagina să nu contacteze Google Fonts).

Rulare:  python3 build.py
"""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "src" / "template.html"
OUTPUT = ROOT / "index.html"
FONTS_DIR = ROOT / "src" / "fonts"
PREFIX = "WhatsApp Image 2026-11-13 at 13.10.42"

# Ordinea corespunde array-ului ARTICLES din template (__IMG1__ ... __IMG5__).
IMAGES = [
    f"{PREFIX} (1).jpeg",  # 1. Prima pagină JCM – AI at the Bedside of Psychiatry
    f"{PREFIX} (2).jpeg",  # 2. Forest plot – meta-analiză
    f"{PREFIX}.jpeg",      # 3. Corelație FSFI–BESAQ
    f"{PREFIX} (3).jpeg",  # 4. Clustere PCA
    f"{PREFIX} (4).jpeg",  # 5. Tabelul 6 – comparații între clustere
]


def fonts_css() -> str:
    """Citește src/fonts/fonts.css și înlocuiește url(fonts/x.woff2) cu data URI."""
    css = (FONTS_DIR / "fonts.css").read_text(encoding="utf-8")

    def embed(m: re.Match) -> str:
        data = base64.b64encode((FONTS_DIR / m.group(1)).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"

    return re.sub(r"url\(fonts/([^)]+\.woff2)\)", embed, css)


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    if "/*__FONTS__*/" not in html:
        raise SystemExit("Eroare: lipsește placeholder-ul /*__FONTS__*/ din template.")
    html = html.replace("/*__FONTS__*/", fonts_css())
    for i, name in enumerate(IMAGES, 1):
        data = base64.b64encode((ROOT / "docs" / name).read_bytes()).decode()
        html = html.replace(f"__IMG{i}__", f"data:image/jpeg;base64,{data}")
    if "__IMG" in html:
        raise SystemExit("Eroare: au rămas placeholder-e __IMGn__ neînlocuite.")
    if "fonts.googleapis.com" in html or "fonts.gstatic.com" in html:
        raise SystemExit("Eroare: pagina încă face referire la Google Fonts.")
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"index.html generat ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
