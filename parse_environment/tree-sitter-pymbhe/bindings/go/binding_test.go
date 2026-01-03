package tree_sitter_pymbhe_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_pymbhe "github.com/tree-sitter/tree-sitter-pymbhe/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_pymbhe.Language())
	if language == nil {
		t.Errorf("Error loading Pymbhe grammar")
	}
}
