from unittest import TestCase

import tree_sitter, tree_sitter_pymbhe


class TestLanguage(TestCase):
    def test_can_load_grammar(self):
        try:
            tree_sitter.Language(tree_sitter_pymbhe.language())
        except Exception:
            self.fail("Error loading Pymbhe grammar")
