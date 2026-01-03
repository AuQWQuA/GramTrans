// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterJavahemp",
    products: [
        .library(name: "TreeSitterJavahemp", targets: ["TreeSitterJavahemp"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterJavahemp",
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
            name: "TreeSitterJavahempTests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterJavahemp",
            ],
            path: "bindings/swift/TreeSitterJavahempTests"
        )
    ],
    cLanguageStandard: .c11
)
