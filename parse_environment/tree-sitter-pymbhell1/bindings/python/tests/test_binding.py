from unittest import TestCase

import tree_sitter, tree_sitter_pymbhell1


class TestLanguage(TestCase):
    def test_can_load_grammar(self):
        try:
            tree_sitter.Language(tree_sitter_pymbhell1.language())
        except Exception:
            self.fail("Error loading Pymbhell1 grammar")
