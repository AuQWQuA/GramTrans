// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterMathqapythonll1",
    products: [
        .library(name: "TreeSitterMathqapythonll1", targets: ["TreeSitterMathqapythonll1"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterMathqapythonll1",
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
            name: "TreeSitterMathqapythonll1Tests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterMathqapythonll1",
            ],
            path: "bindings/swift/TreeSitterMathqapythonll1Tests"
        )
    ],
    cLanguageStandard: .c11
)
