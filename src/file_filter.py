from pathlib import Path

SKIP_FOLDER = {".git", ".github", ".idea", ".vscode", "__pycache__", "node_modules", "vendor", "vendors",
    "dist", "target", "out", "coverage", ".next", ".nuxt", ".venv", "venv", ".circleci"
}

SKIP_FILE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".zip", ".class", ".md", ".txt",
    ".csv", ".json", ".yml", ".yaml", ".lock", ".log", ".ico", ".exe", ".dll", ".so", ".dylib", ".docx",
    ".jar", ".mp4", ".aar", ".bat",
    ".sh", ".example", ".template", ".prisma", ".graphql", ".config",
}

SKIP_NAME_SUFFIXES = {".d.ts"}

INCLUDE_FILENAMES = {"dockerfile", "makefile"}


def should_include_file(file_path: str) -> bool:
    """ Return true if the file should be included for analysis """
    # We change file path from string into object Path using python library
    path = Path(file_path)  # Object Path has a method that can help us to search file and folder recursively

    if any(folder.lower() in SKIP_FOLDER for folder in path.parts):
        return False

    name = path.name.lower()

    if any(name.endswith(suffix) for suffix in SKIP_NAME_SUFFIXES):
        return False

    if name in INCLUDE_FILENAMES:
        return True

    extension = path.suffix.lower()    # Get file extension

    if extension == "":
        return False

    if extension in SKIP_FILE_EXTENSIONS:
        return False

    return True