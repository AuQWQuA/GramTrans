import XCTest
import SwiftTreeSitter
import TreeSitterJavahempll

final class TreeSitterJavahempllTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_javahempll())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Javahempll grammar")
    }
}
