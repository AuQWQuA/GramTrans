import XCTest
import SwiftTreeSitter
import TreeSitterMathqapython

final class TreeSitterMathqapythonTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_mathqapython())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Mathqapython grammar")
    }
}
