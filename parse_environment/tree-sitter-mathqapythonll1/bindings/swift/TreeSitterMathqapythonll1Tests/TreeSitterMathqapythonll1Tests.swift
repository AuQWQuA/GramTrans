import XCTest
import SwiftTreeSitter
import TreeSitterMathqapythonll1

final class TreeSitterMathqapythonll1Tests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_mathqapythonll1())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Mathqapythonll1 grammar")
    }
}
