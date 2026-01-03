// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "TreeSitterJavahempll",
    products: [
        .library(name: "TreeSitterJavahempll", targets: ["TreeSitterJavahempll"]),
    ],
    dependencies: [
        .package(url: "https://github.com/ChimeHQ/SwiftTreeSitter", from: "0.8.0"),
    ],
    targets: [
        .target(
            name: "TreeSitterJavahempll",
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
            name: "TreeSitterJavahempllTests",
            dependencies: [
                "SwiftTreeSitter",
                "TreeSitterJavahempll",
            ],
            path: "bindings/swift/TreeSitterJavahempllTests"
        )
    ],
    cLanguageStandard: .c11
)
