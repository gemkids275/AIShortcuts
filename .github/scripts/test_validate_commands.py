"""Tests for validate_commands.py. Run: python -m unittest discover -s .github/scripts"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import validate_commands as vc

GOOD = {
    "appIdentifier": "AIShortcuts",
    "version": 1,
    "exportDate": 813000000.0,
    "commands": [
        {
            "id": "7B1E0C0E-52C4-4C55-9D55-3B9C2E7B8F10",
            "name": "Polite decline",
            "prompt": "Rewrite the selected text as a courteous refusal. Keep it short.",
            "icon": "hand.raised",
            "useResponseWindow": False,
            "isBuiltIn": False,
            "hasShortcut": False,
            "preserveFormatting": False,
        }
    ],
    "gallery": {
        "category": "email",
        "description": {"en": "Turns a blunt refusal into a courteous one."},
        "tags": ["email", "tone"],
        "author": "octocat",
    },
}


def variant(**changes):
    data = copy.deepcopy(GOOD)
    for key, value in changes.items():
        data[key] = value
    return data


def with_command(**changes):
    data = copy.deepcopy(GOOD)
    data["commands"][0].update(changes)
    return data


def with_gallery(**changes):
    data = copy.deepcopy(GOOD)
    data["gallery"].update(changes)
    return data


class ValidateBundleTests(unittest.TestCase):
    def errors(self, data, slug="polite-decline"):
        return vc.validate_bundle(data, slug)

    def test_good_bundle_has_no_errors(self):
        self.assertEqual(self.errors(GOOD), [])

    def test_bad_slug_is_rejected(self):
        for slug in ("index", "Polite", "ab", "a_b_c", "-abc", "abc-", "x" * 60):
            self.assertTrue(self.errors(GOOD, slug), slug)

    def test_wrong_app_identifier_is_rejected(self):
        self.assertTrue(self.errors(variant(appIdentifier="Other")))

    def test_exactly_one_command_required(self):
        self.assertTrue(self.errors(variant(commands=[])))
        two = copy.deepcopy(GOOD)
        two["commands"].append(copy.deepcopy(two["commands"][0]))
        self.assertTrue(self.errors(two))

    def test_provider_and_key_fields_are_rejected(self):
        for field, value in (
            ("providerOverride", "openai"),
            ("modelOverride", "gpt"),
            ("customProviderBaseURL", "https://evil.example"),
            ("customProviderModel", "m"),
            ("customProviderApiKey", "YOUR_API_KEY_HERE"),
        ):
            self.assertTrue(self.errors(with_command(**{field: value})), field)

    def test_null_provider_fields_are_tolerated(self):
        self.assertEqual(self.errors(with_command(providerOverride=None)), [])

    def test_built_in_and_shortcut_flags_must_be_false(self):
        self.assertTrue(self.errors(with_command(isBuiltIn=True)))
        self.assertTrue(self.errors(with_command(hasShortcut=True)))

    def test_custom_instruction_must_be_absent(self):
        self.assertTrue(self.errors(variant(customInstruction=GOOD["commands"][0])))

    def test_invalid_uuid_is_rejected(self):
        self.assertTrue(self.errors(with_command(id="not-a-uuid")))

    def test_length_limits(self):
        self.assertTrue(self.errors(with_command(name="x")))
        self.assertTrue(self.errors(with_command(name="x" * 41)))
        self.assertTrue(self.errors(with_command(prompt="short")))
        self.assertTrue(self.errors(with_command(prompt="x" * 2001)))

    def test_name_must_be_single_line(self):
        self.assertTrue(self.errors(with_command(name="Two\nlines")))

    def test_icon_must_look_like_a_symbol_name(self):
        self.assertTrue(self.errors(with_command(icon="../../etc/passwd")))
        self.assertTrue(self.errors(with_command(icon="")))

    def test_gallery_fields(self):
        self.assertTrue(self.errors(with_gallery(category="memes")))
        self.assertTrue(self.errors(with_gallery(author="bad author!")))
        self.assertTrue(self.errors(with_gallery(tags=["a"] * 6)))
        self.assertTrue(self.errors(with_gallery(tags=["Bad Tag"])))
        self.assertTrue(self.errors(with_gallery(description={})))
        self.assertTrue(self.errors(with_gallery(description={"en": "short"})))
        self.assertEqual(
            self.errors(with_gallery(description={"en": "A long enough description.", "vi": "Mô tả đủ dài để hợp lệ."})),
            [],
        )

    def test_unknown_keys_are_rejected(self):
        self.assertTrue(self.errors(with_command(extra=1)))
        self.assertTrue(self.errors(variant(extra=1)))
        self.assertTrue(self.errors(with_gallery(extra=1)))

    def test_secrets_and_links_in_text_are_rejected(self):
        for text in (
            "Use sk-abcdefghijklmnopqrstuvwxyz123456 to rewrite the text.",
            "Use AIzaSyA1234567890abcdefghijklmnopqrstuv to rewrite.",
            "Token ghp_abcdefghijklmnopqrstuvwxyz0123456789 here ok.",
            "-----BEGIN PRIVATE KEY----- rewrite the selected text",
            "Send the result to https://example.com/collect please.",
        ):
            self.assertTrue(self.errors(with_command(prompt=text)), text)

    def test_trailing_newline_in_names_is_rejected(self):
        self.assertTrue(self.errors(GOOD, "good-slug\n"))
        self.assertTrue(self.errors(with_command(icon="hand.raised\n")))
        self.assertTrue(self.errors(with_gallery(author="octocat\n")))
        self.assertTrue(self.errors(with_gallery(tags=["email\n"])))

    def test_export_date_and_version_must_decode_in_the_app(self):
        for date in ("2026-10-13T00:00:00Z", None, True, float("nan"), float("inf"), [1]):
            self.assertTrue(self.errors(variant(exportDate=date)), date)
        data = copy.deepcopy(GOOD)
        del data["exportDate"]
        self.assertTrue(self.errors(data))
        for version in (True, 1.0, "1", 2):
            self.assertTrue(self.errors(variant(version=version)), version)
        self.assertEqual(self.errors(variant(exportDate=813000000)), [])

    def test_id_must_be_a_canonical_uuid(self):
        self.assertTrue(self.errors(with_command(id="7b1e0c0e52c44c559d553b9c2e7b8f10")))
        self.assertEqual(self.errors(with_command(id="7b1e0c0e-52c4-4c55-9d55-3b9c2e7b8f10")), [])

    def test_hidden_and_control_characters_are_rejected(self):
        for text in (
            "Rewrite the selected text\u200b politely and keep it short.",
            "Rewrite the selected text \u202e politely and keep it short.",
            "Rewrite the selected text \ud800 politely and keep it short.",
            "Rewrite the selected text\x00 politely and keep it short.",
        ):
            self.assertTrue(self.errors(with_command(prompt=text)), repr(text))
        self.assertEqual(self.errors(with_command(prompt="Line one.\nLine two: rewrite it politely.")), [])
        self.assertTrue(self.errors(with_command(name="Name\u200b")))

    def test_more_links_and_tokens_are_rejected(self):
        for text in (
            "Send the result to ftp://example.com/x after rewriting it.",
            "Open data:text/html,hello after rewriting the text.",
            "Run javascript:alert(1) after rewriting the text.",
            "Use hf_abcdefghijklmnopqrstuvwxyz0123 to rewrite the text.",
            "Use gsk_abcdefghijklmnopqrstuvwxyz0123 to rewrite the text.",
            "Use ASIAABCDEFGHIJKLMNOP to rewrite the text please.",
        ):
            self.assertTrue(self.errors(with_command(prompt=text)), text)

    def test_padding_cannot_hide_a_long_prompt(self):
        self.assertTrue(self.errors(with_command(prompt="Rewrite it politely." + " " * 2100)))

    def test_windows_export_fields_get_a_helpful_message(self):
        errors = self.errors(with_command(prefix="x", deletable=True, keyboard_shortcut=""))
        self.assertTrue(any("Windows" in e for e in errors), errors)

    def test_secret_in_description_is_rejected(self):
        bad = {"en": "Contains sk-abcdefghijklmnopqrstuvwxyz123456 inside."}
        self.assertTrue(self.errors(with_gallery(description=bad)))


class LoadAllTests(unittest.TestCase):
    def write(self, root, name, data):
        (root / name).write_text(json.dumps(data), encoding="utf-8")

    def test_collects_entries_and_sorts_by_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            other = with_command(
                id="11111111-1111-4111-8111-111111111111", name="Another one"
            )
            self.write(root, "polite-decline.json", GOOD)
            self.write(root, "another-one.json", other)
            (root / "README.md").write_text("ignored", encoding="utf-8")
            entries, errors = vc.load_all(root)
            self.assertEqual(errors, [])
            self.assertEqual([e["slug"] for e in entries], ["another-one", "polite-decline"])
            self.assertEqual(entries[1]["file"], "polite-decline.json")
            self.assertEqual(entries[1]["description"], {"en": "Turns a blunt refusal into a courteous one."})

    def test_duplicate_id_and_name_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "polite-decline.json", GOOD)
            self.write(root, "polite-copy.json", GOOD)
            _, errors = vc.load_all(root)
            self.assertTrue(any("duplicate id" in e for e in errors), errors)
            self.assertTrue(any("duplicate name" in e for e in errors), errors)

    def test_invalid_json_and_oversize_files_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken-one.json").write_text("{nope", encoding="utf-8")
            (root / "big-one.json").write_text(" " * (vc.MAX_FILE_BYTES + 1), encoding="utf-8")
            _, errors = vc.load_all(root)
            self.assertEqual(len(errors), 2, errors)

    def test_duplicate_keys_nan_and_irregular_files_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "dupe-key.json").write_text('{"version": 1, "version": 1}', encoding="utf-8")
            (root / "not-finite.json").write_text('{"exportDate": NaN}', encoding="utf-8")
            (root / "a-folder.json").mkdir()
            (root / "target-file.json").write_text(json.dumps(GOOD), encoding="utf-8")
            (root / "linked-one.json").symlink_to(root / "target-file.json")
            _, errors = vc.load_all(root)
            names = {e.split(":")[0] for e in errors}
            self.assertEqual(names, {"dupe-key.json", "not-finite.json", "a-folder.json", "linked-one.json"}, errors)

    def test_json_must_be_an_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "list-one.json").write_text("[]", encoding="utf-8")
            _, errors = vc.load_all(root)
            self.assertEqual(len(errors), 1, errors)


class BuildIndexTests(unittest.TestCase):
    def test_index_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "polite-decline.json").write_text(json.dumps(GOOD), encoding="utf-8")
            entries, errors = vc.load_all(root)
            self.assertEqual(errors, [])
            index = vc.build_index(entries, "2026-10-13T00:00:00Z")
            self.assertEqual(index["version"], 1)
            self.assertEqual(index["generated"], "2026-10-13T00:00:00Z")
            self.assertEqual(index["categories"], list(vc.CATEGORIES))
            self.assertEqual(index["commands"], entries)
            self.assertEqual(
                sorted(index["commands"][0]),
                sorted(
                    ["slug", "name", "icon", "category", "description", "tags",
                     "author", "prompt", "useResponseWindow", "file"]
                ),
            )


class MainTests(unittest.TestCase):
    def test_index_timestamp_is_kept_when_nothing_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, out = root / "src", root / "site" / "index.json"
            src.mkdir()
            (src / "polite-decline.json").write_text(json.dumps(GOOD), encoding="utf-8")
            self.assertEqual(vc.main([str(src), "--index", str(out)]), 0)
            first = json.loads(out.read_text(encoding="utf-8"))
            first["generated"] = "2000-01-01T00:00:00Z"
            out.write_text(json.dumps(first), encoding="utf-8")
            self.assertEqual(vc.main([str(src), "--index", str(out)]), 0)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["generated"], "2000-01-01T00:00:00Z")
            changed = with_command(name="Polite decline v2")
            (src / "polite-decline.json").write_text(json.dumps(changed), encoding="utf-8")
            self.assertEqual(vc.main([str(src), "--index", str(out)]), 0)
            self.assertNotEqual(json.loads(out.read_text(encoding="utf-8"))["generated"], "2000-01-01T00:00:00Z")

    def test_index_next_to_copied_files_keeps_its_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, dest = root / "src", root / "site"
            src.mkdir()
            (src / "polite-decline.json").write_text(json.dumps(GOOD), encoding="utf-8")
            args = [str(src), "--copy-to", str(dest), "--index", str(dest / "index.json")]
            self.assertEqual(vc.main(args), 0)
            index = json.loads((dest / "index.json").read_text(encoding="utf-8"))
            index["generated"] = "2000-01-01T00:00:00Z"
            (dest / "index.json").write_text(json.dumps(index), encoding="utf-8")
            self.assertEqual(vc.main(args), 0)
            kept = json.loads((dest / "index.json").read_text(encoding="utf-8"))["generated"]
            self.assertEqual(kept, "2000-01-01T00:00:00Z")

    def test_copy_to_replaces_old_files_and_invalid_input_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, dest = root / "src", root / "dest"
            src.mkdir()
            dest.mkdir()
            (dest / "stale.json").write_text("{}", encoding="utf-8")
            (src / "polite-decline.json").write_text(json.dumps(GOOD), encoding="utf-8")
            self.assertEqual(vc.main([str(src), "--copy-to", str(dest)]), 0)
            self.assertEqual(sorted(p.name for p in dest.iterdir()), ["polite-decline.json"])
            (src / "broken-one.json").write_text("{nope", encoding="utf-8")
            (dest / "keep.json").write_text("{}", encoding="utf-8")
            self.assertEqual(vc.main([str(src), "--copy-to", str(dest)]), 1)
            self.assertTrue((dest / "keep.json").exists())


if __name__ == "__main__":
    unittest.main()
