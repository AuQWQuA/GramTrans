// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterPymbhell1",
    products: [
        .library(name: "TreeSitterPymbhell1", targets: ["TreeSitterPymbhell1"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterPymbhell1",
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
            name: "TreeSitterPymbhell1Tests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterPymbhell1",
            ],
            path: "bindings/swift/TreeSitterPymbhell1Tests"
        )
    ],
    cLanguageStandard: .c11
)
