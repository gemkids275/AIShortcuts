import gettext
import os
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
