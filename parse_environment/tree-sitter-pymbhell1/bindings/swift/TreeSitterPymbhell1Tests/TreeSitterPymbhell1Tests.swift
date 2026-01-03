import XCTest
import SwiftTreeSitter
import TreeSitterPymbhell1

final class TreeSitterPymbhell1Tests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_pymbhell1())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Pymbhell1 grammar")
    }
}
