import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.command import Command
from models.command_manager import CommandManager


class CommandManagerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(__file__)))
        self.dir = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_restore_built_ins_keeps_custom(self):
        m = CommandManager(self.dir)
        m.load()
        m.add_command(Command(name="Mine", prompt="p", prefix="", icon=""))
        proof = m.get_by_name("Proofread")
        m.delete_command(proof.id)
        self.assertIsNone(m.get_by_name("Proofread"))
        m.restore_built_ins()
        self.assertIsNotNone(m.get_by_name("Proofread"))
        self.assertIsNotNone(m.get_by_name("Mine"))

    def test_legacy_options_migrated(self):
        opts = os.path.join(self.dir, "options.json")
        with open(opts, "w", encoding="utf-8") as f:
            json.dump({
                "Proofread": {"prefix": "x", "instruction": "y", "icon": "i", "open_in_window": False},
                "Haiku": {"prefix": "Haiku:", "instruction": "Write a haiku", "icon": "icons/custom", "open_in_window": True},
                "Custom": {"prefix": "", "instruction": "", "icon": "", "open_in_window": True},
            }, f)
        m = CommandManager(self.dir)
        m.load(legacy_options_paths=[opts])
        haiku = m.get_by_name("Haiku")
        self.assertIsNotNone(haiku)
        self.assertEqual(haiku.prompt, "Write a haiku")
        self.assertTrue(haiku.use_response_window)
        self.assertFalse(haiku.is_built_in)
        self.assertIsNone(m.get_by_name("Custom"))
        self.assertTrue(os.path.exists(os.path.join(self.dir, "commands.json")))

    def test_existing_commands_json_wins_over_legacy(self):
        m = CommandManager(self.dir)
        m.load()
        opts = os.path.join(self.dir, "options.json")
        with open(opts, "w", encoding="utf-8") as f:
            json.dump({"Haiku": {"prefix": "", "instruction": "", "icon": ""}}, f)
        m2 = CommandManager(self.dir)
        m2.load(legacy_options_paths=[opts])
        self.assertIsNone(m2.get_by_name("Haiku"))

    def test_corrupt_commands_json_is_backed_up(self):
        path = os.path.join(self.dir, "commands.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not json")
        m = CommandManager(self.dir)
        m.load()
        self.assertTrue(os.path.exists(path + ".corrupt"))
        self.assertIsNotNone(m.get_by_name("Proofread"))

    def test_claim_shortcut_conflicts(self):
        used = set()
        a = Command(name="a", prompt="", prefix="", icon="", keyboard_shortcut="Ctrl+P")
        b = Command(name="b", prompt="", prefix="", icon="", keyboard_shortcut="ctrl+p")
        c = Command(name="c", prompt="", prefix="", icon="", keyboard_shortcut="ctrl+space")
        d = Command(name="d", prompt="", prefix="", icon="", keyboard_shortcut="ctrl+k")
        for cmd in (a, b, c, d):
            CommandManager.claim_shortcut(cmd, used, "Ctrl+Space")
        self.assertEqual(a.keyboard_shortcut, "Ctrl+P")
        self.assertIsNone(b.keyboard_shortcut)
        self.assertIsNone(c.keyboard_shortcut)
        self.assertEqual(d.keyboard_shortcut, "ctrl+k")


if __name__ == "__main__":
    unittest.main()
