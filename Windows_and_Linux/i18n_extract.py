"""List every translatable string used in the code (calls to _(...) / gettext(...))."""
import ast
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def extract() -> dict[str, str]:
    found: dict[str, str] = {}
    files = ["WritingToolApp.py", "aiprovider.py"] + sorted(glob.glob("ui/*.py", root_dir=ROOT)) + sorted(glob.glob("models/*.py", root_dir=ROOT))
    for rel in files:
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ""
            arg = node.args[0]
            if name in ("_", "gettext") and isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                found.setdefault(arg.value, rel)
    return found


if __name__ == "__main__":
    for msgid, rel in extract().items():
        print(f"{rel}: {msgid!r}")
