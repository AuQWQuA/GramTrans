// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterMathqapythonll2",
    products: [
        .library(name: "TreeSitterMathqapythonll2", targets: ["TreeSitterMathqapythonll2"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterMathqapythonll2",
            dependencies: [],
            path: ".",
            sources: [
                "src/parser.c",
                // NOTE: if your language has an external scanner, add it here.
            ],
            resources: [
                .copy("queries")
            ],
            publicHeadersPath: "bindings/swift",
            cSettings: [.headerSearchPath("src")]
        ),
        .testTarget(
            name: "TreeSitterMathqapythonll2Tests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterMathqapythonll2",
            ],
            path: "bindings/swift/TreeSitterMathqapythonll2Tests"
        )
    ],
    cLanguageStandard: .c11
)
