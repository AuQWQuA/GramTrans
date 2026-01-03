// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterMathqapython",
    products: [
        .library(name: "TreeSitterMathqapython", targets: ["TreeSitterMathqapython"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterMathqapython",
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
            name: "TreeSitterMathqapythonTests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterMathqapython",
            ],
            path: "bindings/swift/TreeSitterMathqapythonTests"
        )
    ],
    cLanguageStandard: .c11
)
