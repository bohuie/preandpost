"""
Size metric extraction using a line-based approximation. 
This module analyzes supported source files and computes: 
- Files 
- Lines
- Lines of Code / ncloc (non-commenting lines of code) 
- Comment lines 
- Comment density 
- Statements 
- Functions 
- Classes 

The scanner filters unsupported, binary, vendor, and build files before analysis. It detects comment syntax based on 
file extension, hide string contents with space to avoid false comment detection, tracks multi-line block comments, 
and uses language-specific regex patterns to estimate statements, functions, and classes.

Limitation:
This implementation uses a line-based approximation. Some metrics may not be detected perfectly because programming 
languages have different syntax formats and language-specific constructs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Iterable


# ---------------------------------------------------------------------------
# File filtering
# ---------------------------------------------------------------------------

SKIP_DIRS = {".git", ".github", ".idea", ".vscode", "__pycache__", "node_modules", "vendor", "vendors",
    "dist", "build", "target", "out", "coverage", ".next", ".nuxt", ".venv", "venv", "env",
}

SKIP_FILE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".zip", ".tar", ".gz",
    ".rar", ".7z", ".exe", ".dll", ".so", ".dylib", ".class", ".jar", ".pyc", ".pyo", ".lock",
}

SOURCE_EXTENSIONS = {".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".c", ".h", ".cpp", ".hpp", ".cc", ".cs",
    ".go", ".rs",".php", ".rb", ".r", ".sh", ".bash", ".zsh", ".sql", ".html", ".xml", ".css", ".scss", ".yaml",
    ".yml", ".toml", ".ini", ".m", ".lua", ".hs", ".swift", ".kt", ".scala", ".dart",
}


# ---------------------------------------------------------------------------
# Comment syntax
# ---------------------------------------------------------------------------

COMMENT_STYLES = {
    "hash": {
        "single": ["#"],
        "block": [],
    },
    "c_style": {
        "single": ["//"],
        "block": [("/*", "*/")],
    },
    "c_style_hash": {
        "single": ["//", "#"],
        "block": [("/*", "*/")],
    },
    "sql": {
        "single": ["--", "#"],
        "block": [("/*", "*/")],
    },
    "html": {
        "single": [],
        "block": [("<!--", "-->")],
    },
    "css": {
        "single": [],
        "block": [("/*", "*/")],
    },
    "python": {
        "single": ["#"],
        "block": [('"""', '"""'), ("'''", "'''")],
    },
    "ruby": {
        "single": ["#"],
        "block": [("=begin", "=end")],
    },
    "lua": {
        "single": ["--"],
        "block": [("--[[", "]]")],
    },
    "haskell": {
        "single": ["--"],
        "block": [("{-", "-}")],
    },
    "matlab": {
        "single": ["%"],
        "block": [("%{", "%}")],
    },
    "config": {
        "single": ["#", ";"],
        "block": [],
    },
}

EXTENSION_TO_STYLE = {
    ".py": "python",
    ".java": "c_style",
    ".js": "c_style",
    ".jsx": "c_style",
    ".ts": "c_style",
    ".tsx": "c_style",
    ".c": "c_style",
    ".h": "c_style",
    ".cpp": "c_style",
    ".hpp": "c_style",
    ".cc": "c_style",
    ".cs": "c_style",
    ".go": "c_style",
    ".rs": "c_style",
    ".swift": "c_style",
    ".kt": "c_style",
    ".scala": "c_style",
    ".dart": "c_style",
    ".php": "c_style_hash",
    ".rb": "ruby",
    ".r": "hash",
    ".sh": "hash",
    ".bash": "hash",
    ".zsh": "hash",
    ".yaml": "hash",
    ".yml": "hash",
    ".toml": "hash",
    ".sql": "sql",
    ".html": "html",
    ".xml": "html",
    ".md": "html",
    ".css": "css",
    ".scss": "c_style",
    ".ini": "config",
    ".m": "matlab",
    ".lua": "lua",
    ".hs": "haskell",
}


# ---------------------------------------------------------------------------
# Regex patterns for approximate structure counting
# ---------------------------------------------------------------------------

CONTROL_FLOW_KEYWORDS = {"if", "else", "elif", "for", "while", "switch", "catch", "try", "finally", "do",
    "case", "return",
}

PYTHON_BLOCK_HEADERS = {"if", "elif", "else", "for", "while", "def", "class", "try", "except", "finally", "with",
    "async", "match", "case",
}

C_STYLE_BLOCK_HEADERS = {"if", "else", "for", "while", "switch", "case", "catch", "try", "finally", "do",
}

FUNCTION_PATTERNS = {
    "python": [
        re.compile(r"^\s*def\s+[A-Za-z_]\w*\s*\("),
        re.compile(r"^\s*async\s+def\s+[A-Za-z_]\w*\s*\("),
    ],
    "javascript": [
        re.compile(r"^\s*function\s+[A-Za-z_]\w*\s*\("),
        re.compile(r"^\s*(const|let|var)\s+[A-Za-z_]\w*\s*=\s*(async\s*)?\([^)]*\)\s*=>"),
        re.compile(r"^\s*(const|let|var)\s+[A-Za-z_]\w*\s*=\s*(async\s*)?[A-Za-z_]\w*\s*=>"),
        re.compile(r"^\s*[A-Za-z_]\w*\s*\([^)]*\)\s*\{"),
    ],
    "c_style": [
        re.compile(
            r"^\s*"
            r"(public|private|protected|internal|static|final|abstract|virtual|override|async|export|extern|\s)*"
            r"[\w:<>,\[\]\*&]+\s+"
            r"[A-Za-z_]\w*\s*"
            r"\([^;]*\)\s*\{"
        ),
    ],
}

CLASS_PATTERNS = {
    "python": [
        re.compile(r"^\s*class\s+[A-Za-z_]\w*"),
    ],
    "javascript": [
        re.compile(r"^\s*(export\s+)?(abstract\s+)?class\s+[A-Za-z_]\w*"),
        re.compile(r"^\s*(export\s+)?interface\s+[A-Za-z_]\w*"),
        re.compile(r"^\s*(export\s+)?enum\s+[A-Za-z_]\w*"),
    ],
    "c_style": [
        re.compile(
            r"^\s*"
            r"(public|private|protected|internal|static|final|abstract|sealed|export|\s)*"
            r"(class|interface|enum|struct|@interface)\s+"
            r"[A-Za-z_]\w*"
        ),
    ],
}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class ScannerState:
    """Tracks whether the scanner is currently inside a block comment."""

    in_block_comment: bool = False
    block_end_marker: str | None = None


@dataclass
class FileSizeMetrics:
    """Stores size metrics for one file."""

    file_path: str
    language: str
    lines: int = 0
    ncloc: int = 0
    comment_lines: int = 0
    comment_density: float = 0.0
    statements: int = 0
    functions: int = 0
    classes: int = 0


@dataclass
class RepositorySizeMetrics:
    """Stores aggregated size metrics for a repository."""

    files: int = 0
    lines: int = 0
    ncloc: int = 0
    comment_lines: int = 0
    comment_density: float = 0.0
    statements: int = 0
    functions: int = 0
    classes: int = 0


# ---------------------------------------------------------------------------
# Language Detection and File Filtering
# ---------------------------------------------------------------------------

def get_file_extension(file_path: str | Path) -> str:
    return Path(file_path).suffix.lower()


def detect_language(file_path: str | Path) -> str:
    """Returns a simple language label based on file extension."""

    extension = get_file_extension(file_path)

    extension_to_language = {
        ".py": "python",
        ".java": "java",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".c": "c",
        ".h": "c/c++",
        ".cpp": "c++",
        ".hpp": "c++",
        ".cc": "c++",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".rb": "ruby",
        ".r": "r",
        ".sh": "shell",
        ".bash": "shell",
        ".zsh": "shell",
        ".sql": "sql",
        ".html": "html",
        ".xml": "xml",
        ".css": "css",
        ".scss": "scss",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".ini": "ini",
        ".m": "matlab",
        ".lua": "lua",
        ".hs": "haskell",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
        ".dart": "dart",
    }

    return extension_to_language.get(extension, "unknown")


def get_comment_style(file_path: str | Path) -> dict[str, list]:
    """Determines the comment format based on the file extension."""

    extension = get_file_extension(file_path)
    style_name = EXTENSION_TO_STYLE.get(extension)      # Gets the style name from the extension.

    if style_name is None:
        return {"single": [], "block": []}

    return COMMENT_STYLES[style_name]


def should_skip_file(file_path: str | Path) -> bool:
    """Skips binary, vendor, build, generated files."""

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in SKIP_FILE_EXTENSIONS:
        return True

    if extension not in SOURCE_EXTENSIONS:
        return True

    lower_parts = {part.lower() for part in path.parts}     # Skip files located in the skipped folder.
    if lower_parts.intersection(SKIP_DIRS):
        return True

    return False


def iter_source_files(root_path: str | Path) -> Iterable[Path]:
    """Yields source files under a repository path."""

    root = Path(root_path)

    if root.is_file():
        if not should_skip_file(root):
            yield root
        return

    for file_path in root.rglob("*"):       # Searches all files and folders in the root, including its subfolders.
        if file_path.is_file() and not should_skip_file(file_path):
            yield file_path


# ---------------------------------------------------------------------------
# Comments and ncloc
# ---------------------------------------------------------------------------

def mask_strings(line: str) -> str:
    """
    Replaces string contents with spaces while preserving line length.

    Example:
        url = "https://example.com"  # comment
    becomes:
        url = "                   "  # comment

    This prevents comment markers inside strings from being detected as comments.
    """

    result = []
    inside_string = False
    quote_char: str | None = None
    escape_next = False

    for char in line:
        if escape_next:
            escape_next = False

            if inside_string:
                result.append(" ")
            else:
                result.append(char)

            continue

        if char == "\\":
            escape_next = True

            if inside_string:
                result.append(" ")
            else:
                result.append(char)

            continue

        if char in {"'", '"'}:
            if not inside_string:
                inside_string = True
                quote_char = char
                result.append(char)
            elif char == quote_char:
                inside_string = False
                quote_char = None
                result.append(char)
            else:
                result.append(" " if inside_string else char)

            continue

        if inside_string:
            result.append(" ")
        else:
            result.append(char)

    return "".join(result)

def find_marker(line: str, markers: list[str]) -> tuple[int, str] | None:
    """
    Finds the first marker in a line.

    This function assumes strings have already been masked, so markers inside
    strings are no longer visible as real markers.
    """

    first_match: tuple[int, str] | None = None

    for marker in markers:
        index = line.find(marker)

        if index == -1:
            continue

        if first_match is None or index < first_match[0]:
            first_match = (index, marker)

    return first_match

def find_first_block_start(line: str, block_markers: list[tuple[str, str]]) -> tuple[int, str, str] | None:
    """
    Finds the first block comment start.

    Special case:
    If the stripped line starts with a block marker, we treat it as a block
    comment/docstring start.
    """

    stripped_line = line.lstrip()
    leading_spaces = len(line) - len(stripped_line)

    # Check block comments that start the line first.
    for start_marker, end_marker in block_markers:
        if stripped_line.startswith(start_marker):
            return leading_spaces, start_marker, end_marker
    
    # Otherwise, search for block comments outside normal strings.
    starts = [start for start, _ in block_markers]
    masked_line = mask_strings(line)
    found = find_marker(masked_line, starts)

    if found is None:
        return None

    index, start_marker = found

    for start, end in block_markers:
        if start == start_marker:
            return index, start, end

    return None


def strip_inline_comment(line: str, single_markers: list[str]) -> tuple[str, bool, bool]:
    """
    Removes inline comment text if comment marker appears outside strings.

    Returns:
        cleaned_line: code before the comment marker
        has_comment: whether a comment marker was found
        is_comment_only: whether the whole line is a comment
    """

    masked_line = mask_strings(line)        # String contents are hidden with spaces.
    found = find_marker(masked_line, single_markers)

    if found is None:
        return line, False, False

    index, _ = found
    code_before_comment = line[:index]

    if code_before_comment.strip() == "":
        return "", True, True

    return code_before_comment, True, False


def process_line(line: str, state: ScannerState, comment_style: dict[str, list],) -> tuple[str, bool, bool]:
    """
    Processes one line and returns:
        cleaned_code: remaining code after removing comments
        is_comment_line: whether the line should count as comment line
        has_code: whether the line contains code/ncloc
    """

    stripped_line = line.strip()

    if stripped_line == "":
        return "", False, False

    block_markers: list[tuple[str, str]] = comment_style.get("block", [])
    single_markers: list[str] = comment_style.get("single", [])

    if state.in_block_comment:
        end_marker = state.block_end_marker

        if end_marker is None:
            return "", True, False

        end_index = line.find(end_marker)

        if end_index == -1:
            return "", True, False

        state.in_block_comment = False
        state.block_end_marker = None

        text_after_block = line[end_index + len(end_marker):]
        text_after_block, _, _ = strip_inline_comment(text_after_block, single_markers)

        return text_after_block, True, text_after_block.strip() != ""

    block_start = find_first_block_start(line, block_markers)

    if block_start is not None:
        start_index, start_marker, end_marker = block_start
        before_block = line[:start_index]
        after_start = line[start_index + len(start_marker):]

        end_index = after_start.find(end_marker)

        if end_index == -1:
            # Code before a block comment still counts as ncloc.
            state.in_block_comment = True
            state.block_end_marker = end_marker

            before_block, _, _ = strip_inline_comment(before_block, single_markers)
            return before_block, True, before_block.strip() != ""

        # Single-line block comment. Keep code before and after the block.
        after_block = after_start[end_index + len(end_marker):]
        remaining_code = before_block + " " + after_block
        remaining_code, _, _ = strip_inline_comment(remaining_code, single_markers)

        return remaining_code, True, remaining_code.strip() != ""

    cleaned_line, has_comment, is_comment_only = strip_inline_comment(line, single_markers)

    if is_comment_only:
        return "", True, False

    if has_comment:
        return cleaned_line, False, cleaned_line.strip() != ""

    return line, False, True


# ---------------------------------------------------------------------------
# Functions, Classes, Statements
# ---------------------------------------------------------------------------

def get_pattern_group(language: str) -> str | None:
    """Maps language label to regex pattern group."""
    if language == "python":
        return "python"

    if language in {"javascript", "typescript"}:
        return "javascript"

    if language in {"java", "c", "c++", "csharp", "go", "rust", "swift", "kotlin", "scala", "dart"}:
        return "c_style"

    return None


def starts_with_control_flow(clean_line: str) -> bool:
    first_token_match = re.match(r"^\s*([A-Za-z_]\w*)", clean_line)
    if first_token_match is None:
        return False

    return first_token_match.group(1) in CONTROL_FLOW_KEYWORDS


def get_first_token(line: str) -> str:
    """Returns the first identifier-like token in a line."""
    match = re.match(r"^\s*([A-Za-z_]\w*)", line)
    return match.group(1) if match else ""


def count_functions(clean_line: str, language: str) -> int:
    """Count function using regex."""

    masked_line = mask_strings(clean_line)
    pattern_group = get_pattern_group(language)

    if starts_with_control_flow(masked_line):
        return 0

    for pattern in FUNCTION_PATTERNS.get(pattern_group, []):
        if pattern.search(masked_line):
            return 1

    return 0


def count_classes(clean_line: str, language: str) -> int:
    """Count class using regex."""

    masked_line = mask_strings(clean_line)
    pattern_group = get_pattern_group(language)

    for pattern in CLASS_PATTERNS.get(pattern_group, []):
        if pattern.search(masked_line):
            return 1

    return 0


def count_statements(clean_line: str, language: str) -> int:
    """
    For C-style languages, this counts semicolons outside strings.
    For Python, this counts executable lines and simple statements separated by semicolons.
    """

    line = mask_strings(clean_line).strip()

    if line == "":
        return 0

    first_token = get_first_token(line)

    if language == "python":
        if line.endswith(":") and first_token in PYTHON_BLOCK_HEADERS:
            return 0

        return max(1, line.count(";") + 1)

    # Do not count semicolons inside control-flow block headers.
    # Example: for (int i = 0; i < 10; i++) {
    if first_token in C_STYLE_BLOCK_HEADERS:
        return 0

    semicolon_count = line.count(";")
    if semicolon_count > 0:
        return semicolon_count

    if language in {"go", "ruby", "r", "shell", "yaml", "toml"}:
        return 1

    return 0


# ---------------------------------------------------------------------------
# Main metric detectors (also count Files, Lines, Comment Density)
# ---------------------------------------------------------------------------

def analyze_file(file_path: str | Path) -> FileSizeMetrics:
    """Computes size metrics for one file."""

    path = Path(file_path)

    if should_skip_file(path):
        raise ValueError(f"Unsupported or skipped file: {path}")

    language = detect_language(path)
    comment_style = get_comment_style(path)
    state = ScannerState()

    metrics = FileSizeMetrics(file_path=str(path), language=language)

    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError as error:
        raise OSError(f"Could not read file: {path}") from error

    for line in lines:
        metrics.lines += 1

        cleaned_code, is_comment_line, has_code = process_line(
            line=line,
            state=state,
            comment_style=comment_style,
        )

        if is_comment_line:
            metrics.comment_lines += 1

        if has_code:
            metrics.ncloc += 1
            metrics.statements += count_statements(cleaned_code, language)
            metrics.functions += count_functions(cleaned_code, language)
            metrics.classes += count_classes(cleaned_code, language)

    denominator = metrics.ncloc + metrics.comment_lines
    metrics.comment_density = round(
        (metrics.comment_lines / denominator) * 100,
        2,
    ) if denominator > 0 else 0.0

    return metrics


def analyze_repository(root_path: str | Path) -> tuple[RepositorySizeMetrics, list[FileSizeMetrics]]:
    """
    Computes size metrics for all supported source files in a repository.

    Returns:
        repository_metrics: aggregated totals
        file_metrics: per-file results
    """

    repository_metrics = RepositorySizeMetrics()
    file_metrics: list[FileSizeMetrics] = []

    for file_path in iter_source_files(root_path):
        metrics = analyze_file(file_path)
        file_metrics.append(metrics)

        repository_metrics.files += 1
        repository_metrics.lines += metrics.lines
        repository_metrics.ncloc += metrics.ncloc
        repository_metrics.comment_lines += metrics.comment_lines
        repository_metrics.statements += metrics.statements
        repository_metrics.functions += metrics.functions
        repository_metrics.classes += metrics.classes

    denominator = repository_metrics.ncloc + repository_metrics.comment_lines
    repository_metrics.comment_density = round(
        (repository_metrics.comment_lines / denominator) * 100,
        2,
    ) if denominator > 0 else 0.0

    return repository_metrics, file_metrics


def file_metrics_to_dict(metrics: FileSizeMetrics) -> dict:
    return asdict(metrics)


def repository_metrics_to_dict(metrics: RepositorySizeMetrics) -> dict:
    return asdict(metrics)
