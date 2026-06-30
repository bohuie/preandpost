from pathlib import Path

SKIP_FOLDER = {".git", ".github", ".idea", ".vscode", "__pycache__", "node_modules", "vendor", "vendors",
    "dist", "target", "out", "coverage", ".next", ".nuxt", ".venv", "venv", ".circleci", "build",  "third_party",
    "third-party", "external", "externals",  "bower_components", "docs", "documentation", "research", "test", "tests",
    "e2e", "phptest",
}

SKIP_FILE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".zip", ".class", ".md", ".txt",
    ".csv", ".json", ".yml", ".yaml", ".lock", ".log", ".ico", ".exe", ".dll", ".so", ".dylib", ".docx",
    ".jar", ".mp4", ".aar", ".bat", ".sh", ".example", ".template", ".prisma", ".graphql", ".config", ".map",
    ".sql", ".xml", ".tex", ".asta", ".bak", ".psd", ".pptx", ".doc",
}

SKIP_NAME_SUFFIXES = { ".d.ts",
    ".min.js", ".min.css", ".bundle.js", ".bundle.css", "-min.js", "-min.css",  # JavaScript/CSS generated files
    ".spec.ts", ".spec.js", ".test.ts", ".test.js",                             # TypeScript and JavaScript tests
    "_test.php", "test.php",                                                    # PHP tests
    "test.java", "mock.java",                                                   # Java tests and mocks
    "karma.conf.js", "protractor.conf.js", "test.ts", "phpunit.xml",            # Test/configuration entry points
}

INCLUDE_FILENAMES = {"dockerfile", "makefile"}

THIRD_PARTY_SIGNATURE_GROUPS = {
    "leaflet": {
        "leaflet",
        "leafletjs.com",
        "vladimir agafonkin",
    },
    "jquery": {
        "jquery javascript library",
        "jquery.org/license",
    },
    "bootstrap": {
        "bootstrap",
        "getbootstrap.com",
    },
    "php-jwt": {
        "firebase php-jwt",
        "github.com/firebase/php-jwt",
    },
}


def should_include_file(
    file_path: str,
    content: str = "",
) -> bool:
    """
    Return True when a file should be included in student-code analysis.

    Filtering is based on:
    - excluded folders;
    - excluded file suffixes;
    - excluded file extensions;
    - known third-party library signatures.
    """
    path = Path(file_path)

    path_parts = {
        part.lower()
        for part in path.parts
    }

    if path_parts & SKIP_FOLDER:
        return False

    name = path.name.lower()

    if any(
        name.endswith(suffix)
        for suffix in SKIP_NAME_SUFFIXES
    ):
        return False

    if name in INCLUDE_FILENAMES:
        return True

    extension = path.suffix.lower()

    if extension == "":
        return False

    if extension in SKIP_FILE_EXTENSIONS:
        return False

    # Check only the beginning of the file because third-party
    # copyright and library information usually appears in the header.
    content_header = content[:5000].lower()

    for signatures in THIRD_PARTY_SIGNATURE_GROUPS.values():
        matched_signatures = sum(
            signature in content_header
            for signature in signatures
        )

        # Require at least two indicators to reduce false positives.
        if matched_signatures >= 2:
            return False

    return True