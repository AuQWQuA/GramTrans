package tree_sitter_mathqapython_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_mathqapython "github.com/tree-sitter/tree-sitter-mathqapython/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_mathqapython.Language())
	if language == nil {
		t.Errorf("Error loading Mathqapython grammar")
	}
}
