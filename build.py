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
# Logo decupat din docs/logo.jpeg, cu fundal transparent (placeholder __LOGO__ în header).
# PNG transparent, nu JPEG + mix-blend-mode: Safari pe iPhone afișa un dreptunghi alb.
LOGO = ROOT / "src" / "img" / "logo.png"

# Ordinea corespunde array-ului ARTICLES din template (__IMG1__ ... __IMG5__).
IMAGES = [
    "articol-jcm-ai-psihiatrie.jpeg",   # 1. Prima pagină JCM – AI at the Bedside of Psychiatry
    "meta-analiza-forest-plot.jpeg",    # 2. Forest plot – meta-analiză
    "corelatie-fsfi-besaq.jpeg",        # 3. Corelație FSFI–BESAQ
    "clustere-pca.jpeg",                # 4. Clustere PCA
    "tabel-comparatii-clustere.jpeg",   # 5. Tabelul 6 – comparații între clustere
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
    if "__LOGO__" not in html:
        raise SystemExit("Eroare: lipsește placeholder-ul __LOGO__ din template.")
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    html = html.replace("__LOGO__", f"data:image/png;base64,{logo}")
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
