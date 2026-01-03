package tree_sitter_mathqapythoncsg_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_mathqapythoncsg "github.com/tree-sitter/tree-sitter-mathqapythoncsg/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_mathqapythoncsg.Language())
	if language == nil {
		t.Errorf("Error loading Mathqapythoncsg grammar")
	}
}
