/**
 * @file Mathqapythoncsg grammar for tree-sitter
 * @author zz
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: "mathqapythoncsg",

  rules: {
    // TODO: add the actual grammar rules
    source_file: $ => "hello"
  }
});
