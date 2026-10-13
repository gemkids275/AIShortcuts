#!/usr/bin/env python3
"""Validate the community command gallery and build its index.

Usage: validate_commands.py <commands_dir> [--index OUT.json] [--copy-to DIR]

Every <slug>.json in <commands_dir> is an import file for AI Shortcuts (the same
bundle the apps export, one command) plus a "gallery" block with listing metadata.
Files are untrusted community input, so the rules are strict: no provider or key
fields (an imported command must never redirect text to another server), no links,
no key-like strings. Non-.json files (README.md, ...) are ignored.

With --index the index the website reads is written; with --copy-to the validated
files are copied next to it. Both only happen when every file is valid.
"""
import argparse
import json
import re
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = ("writing", "email", "translation", "summarizing", "coding", "learning", "productivity")
MAX_FILE_BYTES = 16 * 1024

SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ICON = re.compile(r"^[a-z0-9]+(\.[a-z0-9]+)*$")
TAG = re.compile(r"^[a-z0-9-]{2,20}$")
AUTHOR = re.compile(r"^[A-Za-z0-9-]{1,39}$")
SECRET = re.compile(
    r"sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*KEY-----|Bearer\s+[A-Za-z0-9._-]{20,}"
)
LINK = re.compile(r"(?i)\b(?:https?|ftp)://|\bwww\.")

TOP_KEYS = {"appIdentifier", "version", "exportDate", "commands", "gallery"}
COMMAND_KEYS = {
    "id", "name", "prompt", "icon", "useResponseWindow", "isBuiltIn", "hasShortcut", "preserveFormatting",
}
# Present only to be rejected unless null (an exporter may write them as null).
FORBIDDEN_COMMAND_KEYS = {
    "providerOverride", "modelOverride", "customProviderBaseURL", "customProviderModel", "customProviderApiKey",
}
GALLERY_KEYS = {"category", "description", "tags", "author"}


def _text_problems(label, text):
    problems = []
    if SECRET.search(text):
        problems.append(f"{label} contains a key- or token-like string")
    if LINK.search(text):
        problems.append(f"{label} contains a link")
    return problems


def _check_text(errors, label, value, low, high, single_line=False):
    if not isinstance(value, str) or not low <= len(value.strip()) <= high:
        errors.append(f"{label} must be a string of {low}-{high} characters")
        return
    if single_line and ("\n" in value or "\r" in value):
        errors.append(f"{label} must be a single line")
    errors.extend(_text_problems(label, value))


def _validate_command(errors, command):
    if not isinstance(command, dict):
        errors.append("commands[0] must be an object")
        return
    for key in command:
        if key in FORBIDDEN_COMMAND_KEYS:
            if command[key] is not None:
                errors.append(f"command.{key} is not allowed in shared commands")
        elif key not in COMMAND_KEYS:
            errors.append(f"command has unknown key '{key}'")
    try:
        uuid.UUID(str(command.get("id")))
    except ValueError:
        errors.append("command.id must be a UUID")
    _check_text(errors, "command.name", command.get("name"), 2, 40, single_line=True)
    _check_text(errors, "command.prompt", command.get("prompt"), 10, 2000)
    icon = command.get("icon")
    if not isinstance(icon, str) or len(icon) > 64 or not ICON.match(icon):
        errors.append("command.icon must be an SF Symbol name such as 'text.badge.checkmark'")
    for key in ("useResponseWindow", "preserveFormatting"):
        if not isinstance(command.get(key, False), bool):
            errors.append(f"command.{key} must be true or false")
    for key in ("isBuiltIn", "hasShortcut"):
        if command.get(key, False) is not False:
            errors.append(f"command.{key} must be false")


def _validate_gallery(errors, gallery):
    if not isinstance(gallery, dict):
        errors.append("gallery block is required")
        return
    for key in gallery:
        if key not in GALLERY_KEYS:
            errors.append(f"gallery has unknown key '{key}'")
    if gallery.get("category") not in CATEGORIES:
        errors.append(f"gallery.category must be one of {', '.join(CATEGORIES)}")
    description = gallery.get("description")
    if not isinstance(description, dict) or "en" not in description:
        errors.append("gallery.description.en is required")
    else:
        for lang, text in description.items():
            if lang not in ("en", "vi"):
                errors.append(f"gallery.description has unknown language '{lang}'")
            else:
                _check_text(errors, f"gallery.description.{lang}", text, 10, 160, single_line=True)
    tags = gallery.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 5 or not all(isinstance(t, str) and TAG.match(t) for t in tags):
        errors.append("gallery.tags must be up to 5 lowercase words (a-z, 0-9, '-', 2-20 characters)")
    author = gallery.get("author")
    if not isinstance(author, str) or not AUTHOR.match(author):
        errors.append("gallery.author must be your GitHub username")


def validate_bundle(data, slug):
    """Return a list of problems for one parsed command file (empty when valid)."""
    errors = []
    if slug == "index" or not SLUG.match(slug) or not 3 <= len(slug) <= 48:
        errors.append("file name must be 3-48 lowercase letters, digits or '-' (e.g. polite-decline.json)")
    if not isinstance(data, dict):
        return errors + ["top level must be a JSON object"]
    for key in data:
        if key not in TOP_KEYS:
            errors.append(f"unknown top-level key '{key}'")
    if data.get("appIdentifier") != "AIShortcuts":
        errors.append("appIdentifier must be 'AIShortcuts'")
    if data.get("version") != 1:
        errors.append("version must be 1")
    commands = data.get("commands")
    if not isinstance(commands, list) or len(commands) != 1:
        errors.append("commands must contain exactly one command")
    else:
        _validate_command(errors, commands[0])
    _validate_gallery(errors, data.get("gallery"))
    return errors


def load_all(directory):
    """Validate every *.json in the directory. Returns (index entries sorted by name, errors)."""
    entries, errors = [], []
    seen_ids, seen_names = {}, {}
    for path in sorted(Path(directory).glob("*.json")):
        slug = path.stem
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.name}: larger than {MAX_FILE_BYTES // 1024} KB")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: not valid UTF-8 JSON ({exc})")
            continue
        problems = validate_bundle(data, slug)
        if problems:
            errors.extend(f"{path.name}: {problem}" for problem in problems)
            continue
        command, gallery = data["commands"][0], data["gallery"]
        cmd_id, name = str(uuid.UUID(command["id"])), command["name"].strip().casefold()
        if cmd_id in seen_ids:
            errors.append(f"{path.name}: duplicate id (also used by {seen_ids[cmd_id]})")
        if name in seen_names:
            errors.append(f"{path.name}: duplicate name (also used by {seen_names[name]})")
        seen_ids.setdefault(cmd_id, path.name)
        seen_names.setdefault(name, path.name)
        entries.append({
            "slug": slug,
            "name": command["name"].strip(),
            "icon": command["icon"],
            "category": gallery["category"],
            "description": gallery["description"],
            "tags": gallery.get("tags", []),
            "author": gallery["author"],
            "prompt": command["prompt"],
            "useResponseWindow": bool(command.get("useResponseWindow", False)),
            "file": path.name,
        })
    entries.sort(key=lambda e: e["name"].casefold())
    return entries, errors


def build_index(entries, generated):
    return {"version": 1, "generated": generated, "categories": list(CATEGORIES), "commands": entries}


def _keep_generated(path, index):
    """Keep the previous timestamp when nothing else changed, so re-runs produce no diff."""
    try:
        previous = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return index["generated"]
    if isinstance(previous, dict) and {**previous, "generated": ""} == {**index, "generated": ""}:
        return previous.get("generated", index["generated"])
    return index["generated"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("directory")
    parser.add_argument("--index", help="write the website index to this file")
    parser.add_argument("--copy-to", help="copy the validated files into this directory")
    args = parser.parse_args(argv)

    entries, errors = load_all(args.directory)
    if errors:
        for error in errors:
            print(f"::error::{error}")
        return 1
    print(f"{len(entries)} command(s) valid.")
    if args.copy_to:
        target = Path(args.copy_to)
        target.mkdir(parents=True, exist_ok=True)
        for old in target.glob("*.json"):
            old.unlink()
        for entry in entries:
            shutil.copyfile(Path(args.directory) / entry["file"], target / entry["file"])
    if args.index:
        out = Path(args.index)
        out.parent.mkdir(parents=True, exist_ok=True)
        generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        index = build_index(entries, generated)
        index["generated"] = _keep_generated(out, index)
        out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
