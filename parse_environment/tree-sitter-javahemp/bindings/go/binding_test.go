package tree_sitter_javahemp_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_javahemp "github.com/tree-sitter/tree-sitter-javahemp/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_javahemp.Language())
	if language == nil {
		t.Errorf("Error loading Javahemp grammar")
	}
}
