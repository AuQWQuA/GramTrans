package tree_sitter_pymbhell1_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_pymbhell1 "github.com/tree-sitter/tree-sitter-pymbhell1/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_pymbhell1.Language())
	if language == nil {
		t.Errorf("Error loading Pymbhell1 grammar")
	}
}
