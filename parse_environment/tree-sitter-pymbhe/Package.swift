// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterPymbhe",
    products: [
        .library(name: "TreeSitterPymbhe", targets: ["TreeSitterPymbhe"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterPymbhe",
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
            name: "TreeSitterPymbheTests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterPymbhe",
            ],
            path: "bindings/swift/TreeSitterPymbheTests"
        )
    ],
    cLanguageStandard: .c11
)
