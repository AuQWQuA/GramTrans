import XCTest
import SwiftTreeSitter
import TreeSitterPymbhe

final class TreeSitterPymbheTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_pymbhe())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Pymbhe grammar")
    }
}
