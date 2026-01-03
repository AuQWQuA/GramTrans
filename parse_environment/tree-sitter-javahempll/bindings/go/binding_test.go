package tree_sitter_javahempll_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_javahempll "github.com/tree-sitter/tree-sitter-javahempll/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_javahempll.Language())
	if language == nil {
		t.Errorf("Error loading Javahempll grammar")
	}
}
