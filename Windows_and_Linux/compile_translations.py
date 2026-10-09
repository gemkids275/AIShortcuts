"""Compile locales/*/LC_MESSAGES/messages.po into messages.mo (needs `polib`).

The .mo files are build artifacts (git-ignored), so the build runs this first.
Usage: python compile_translations.py
"""
import sys
from pathlib import Path

import polib

LOCALES_DIR = Path(__file__).resolve().parent / "locales"


def compile_all() -> list[Path]:
    compiled = []
    for po_path in sorted(LOCALES_DIR.glob("*/LC_MESSAGES/messages.po")):
        mo_path = po_path.with_suffix(".mo")
        polib.pofile(str(po_path), encoding="utf-8").save_as_mofile(str(mo_path))
        compiled.append(mo_path)
    return compiled


if __name__ == "__main__":
    files = compile_all()
    if not files:
        sys.exit(f"No .po files found under {LOCALES_DIR}")
    for f in files:
        print(f"compiled {f.relative_to(LOCALES_DIR.parent)}")
