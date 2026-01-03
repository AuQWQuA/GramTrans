import XCTest
import SwiftTreeSitter
import TreeSitterMathqapythonll2

final class TreeSitterMathqapythonll2Tests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_mathqapythonll2())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Mathqapythonll2 grammar")
    }
}
