package tree_sitter_mathqapythonll1_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_mathqapythonll1 "github.com/tree-sitter/tree-sitter-mathqapythonll1/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_mathqapythonll1.Language())
	if language == nil {
		t.Errorf("Error loading Mathqapythonll1 grammar")
	}
}
