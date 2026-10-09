import gettext
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import compile_translations


class TranslationTests(unittest.TestCase):
    def test_every_locale_compiles_and_translates(self):
        compiled = compile_translations.compile_all()
        langs = {p.parents[1].name for p in compiled}
        self.assertTrue({"en", "it", "ja", "vi", "zh"} <= langs)
        locales = str(compile_translations.LOCALES_DIR)
        vi = gettext.translation("messages", localedir=locales, languages=["vi"])
        self.assertNotEqual(vi.gettext("Save Settings"), "Save Settings")
        self.assertNotEqual(vi.gettext("General Settings"), "General Settings")


if __name__ == "__main__":
    unittest.main()


class TestCoverage(unittest.TestCase):
    def test_every_code_msgid_translated_in_every_locale(self):
        import polib
        from compile_translations import LOCALES_DIR
        from i18n_extract import extract
        ids = extract()
        for po_path in sorted(Path(LOCALES_DIR).glob("*/LC_MESSAGES/messages.po")):
            entries = {e.msgid: e.msgstr for e in polib.pofile(str(po_path))}
            missing = [m for m in ids if not entries.get(m)]
            self.assertEqual(missing, [], f"{po_path.parent.parent.name}: {len(missing)} untranslated")
