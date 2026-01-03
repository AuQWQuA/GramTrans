/**
 * @file Javahemp grammar for tree-sitter
 * @author zz
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: "javahemp",

  rules: {
    // TODO: add the actual grammar rules
    source_file: $ => "hello"
  }
});
