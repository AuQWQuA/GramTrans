import XCTest
import SwiftTreeSitter
import TreeSitterJavahemp

final class TreeSitterJavahempTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_javahemp())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Javahemp grammar")
    }
}
