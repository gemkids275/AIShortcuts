import os
import sys
import unittest
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtWidgets

import aiprovider


class GeminiModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._qapp = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def _provider(self):
        return aiprovider.GeminiProvider(SimpleNamespace(config={}, _=lambda s: s))

    def test_default_model_is_not_retired(self):
        p = self._provider()
        p.load_config({})
        self.assertEqual(p.model_name, "gemma-4-31b-it")

    def test_retired_models_are_migrated(self):
        for old, new in aiprovider.GeminiProvider._RETIRED_MODELS.items():
            p = self._provider()
            p.load_config({"model_name": old})
            self.assertEqual(p.model_name, new)

    def test_custom_model_is_kept(self):
        p = self._provider()
        p.load_config({"model_name": "gemini-3-pro-preview"})
        self.assertEqual(p.model_name, "gemini-3-pro-preview")


if __name__ == "__main__":
    unittest.main()
