"""Bump the Windows/Linux release version everywhere it is hard-coded.

Usage: python bump_version.py <N>      (N = positive integer, greater than current)

Updates update_checker.py, Latest_Version_for_Update_Check.txt and version_info.txt.
Then: commit, merge to main, and push tag `win-v<N>` to trigger the release workflow.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _sub(path: Path, pattern: str, repl: str, expected: int = 1) -> None:
    data = path.read_bytes().decode("utf-8")  # bytes -> str keeps CRLF/LF untouched
    new, count = re.subn(pattern, repl, data)
    if count != expected:
        raise SystemExit(f"{path.name}: expected {expected} match(es) for {pattern!r}, found {count}")
    path.write_bytes(new.encode("utf-8"))


def current_version() -> int:
    text = (ROOT / "update_checker.py").read_text(encoding="utf-8")
    match = re.search(r"^CURRENT_VERSION\s*=\s*(\d+)", text, re.M)
    if not match:
        raise SystemExit("CURRENT_VERSION not found in update_checker.py")
    return int(match.group(1))


def bump(new: int) -> None:
    old = current_version()
    if new <= old:
        raise SystemExit(f"New version {new} must be greater than current {old}")

    _sub(ROOT / "update_checker.py", r"(?m)^CURRENT_VERSION = \d+", f"CURRENT_VERSION = {new}")
    _sub(ROOT / "update_checker.py", r'(?m)^VERSION_STR = "[^"]*"', f'VERSION_STR = "{new}"')
    _sub(ROOT / "Latest_Version_for_Update_Check.txt", r"\d+", str(new))

    info = ROOT / "version_info.txt"
    _sub(info, r"(filevers|prodvers)=\(\d+, 0, 0, 0\)", rf"\1=({new}, 0, 0, 0)", expected=2)
    _sub(info, r"u'(FileVersion|ProductVersion)', u'\d+\.0\.0'", rf"u'\1', u'{new}.0.0'", expected=2)
    print(f"Bumped {old} -> {new}. Next: commit, merge to main, then `git tag win-v{new} && git push origin win-v{new}`.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        raise SystemExit(__doc__)
    bump(int(sys.argv[1]))
