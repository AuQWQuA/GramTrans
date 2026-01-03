import XCTest
import SwiftTreeSitter
import TreeSitterMathqapythoncsg

final class TreeSitterMathqapythoncsgTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_mathqapythoncsg())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Mathqapythoncsg grammar")
    }
}
