from pathlib import Path
import pytest
from src.metrics.size import analyze_file, analyze_repository


def write_file(path: Path, content: str) -> Path:
    """Create a temporary source file for testing."""
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def test_python_basic_metrics(tmp_path: Path):
    """Count basic Python lines, comments, ncloc, functions, classes, and comment density."""
    test_file = write_file(
        tmp_path / "example.py",
        """
# This is a comment

def hello():
    x = 5  # inline comment
    url = "https://example.com"
    return x
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 6
    assert result.comment_lines == 1
    assert result.ncloc == 4
    assert result.functions == 1
    assert result.classes == 0
    assert result.comment_density == 20.0


def test_python_hash_inside_string(tmp_path: Path):
    """Ensure # inside a Python string is not counted as a comment."""
    test_file = write_file(
        tmp_path / "example.py",
        """
value = "# not a comment"
text = "hello # still not a comment"
# real comment
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 3
    assert result.ncloc == 2
    assert result.comment_lines == 1


def test_python_inline_comment(tmp_path: Path):
    """Ensure an inline Python comment counts as ncloc, not as a comment-only line."""
    test_file = write_file(
        tmp_path / "example.py",
        """
x = 10  # inline comment
y = 20
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 2
    assert result.ncloc == 2
    assert result.comment_lines == 0


def test_python_triple_double_quote(tmp_path: Path):
    """Count a Python triple-double-quoted docstring as block-comment lines."""
    test_file = write_file(
        tmp_path / "example.py",
        '''
"""
Module-level explanation.
More explanation.
"""

x = 5
''',
    )

    result = analyze_file(test_file)

    assert result.lines == 6
    assert result.comment_lines == 4
    assert result.ncloc == 1


def test_python_triple_single_quote(tmp_path: Path):
    """Count a Python triple-single-quoted docstring as block-comment lines."""
    test_file = write_file(
        tmp_path / "example.py",
        """
'''
Comment block.
'''
x = 1
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 4
    assert result.comment_lines == 3
    assert result.ncloc == 1


def test_python_escaped_quote(tmp_path: Path):
    """Ensure an escaped quote does not close a Python string too early."""
    test_file = write_file(
        tmp_path / "example.py",
        r'''
text = "She said \"hello # not comment\""
# real comment
''',
    )

    result = analyze_file(test_file)

    assert result.lines == 2
    assert result.ncloc == 1
    assert result.comment_lines == 1


def test_python_single_quote_string(tmp_path: Path):
    """Ensure # inside a single-quoted Python string is not counted as a comment."""
    test_file = write_file(
        tmp_path / "example.py",
        """
text = '# not a comment'
# real comment
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 2
    assert result.ncloc == 1
    assert result.comment_lines == 1


def test_js_url_inside_string(tmp_path: Path):
    """Ensure // inside a JavaScript URL string is not counted as a comment."""
    test_file = write_file(
        tmp_path / "example.js",
        """
// real comment
const url = "https://example.com";
const text = "hello // not a comment";
const x = 5; // inline comment
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 4
    assert result.comment_lines == 1
    assert result.ncloc == 3
    assert result.statements >= 3


def test_js_block_comment_with_code(tmp_path: Path):
    """Count a JavaScript block comment while preserving code after the block."""
    test_file = write_file(
        tmp_path / "example.js",
        """
/* block comment */
const x = 5;
/* comment */ const y = 10;
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 3
    assert result.comment_lines == 2
    assert result.ncloc == 2


def test_js_multiline_block_comment(tmp_path: Path):
    """Count each line inside a JavaScript multi-line block comment."""
    test_file = write_file(
        tmp_path / "example.js",
        """
/*
This is a block comment.
Still comment.
*/
const x = 5;
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 5
    assert result.comment_lines == 4
    assert result.ncloc == 1


def test_js_functions_and_classes(tmp_path: Path):
    """Detect JavaScript classes, methods, regular functions, and arrow functions."""
    test_file = write_file(
        tmp_path / "example.js",
        """
class UserService {
  getUser() {
    return {};
  }
}

function helper() {
  return true;
}

const arrow = () => {
  return false;
};
""",
    )

    result = analyze_file(test_file)

    assert result.classes >= 1
    assert result.functions >= 2
    assert result.ncloc > 0


def test_js_template_literal(tmp_path: Path):
    """Ensure // inside a JavaScript template literal is not counted as a comment-only line."""
    test_file = write_file(
        tmp_path / "example.js",
        """
const url = `https://example.com`;
const message = `hello // not comment`;
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 0
    assert result.ncloc == 2


def test_java_comments(tmp_path: Path):
    """Count Java single-line and block comments while detecting classes and methods."""
    test_file = write_file(
        tmp_path / "Example.java",
        """
// class comment
public class Example {
    /* field comment */
    private int x = 5;

    public void run() {
        System.out.println(x); // inline comment
    }
}
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 2
    assert result.classes >= 1
    assert result.functions >= 1
    assert result.ncloc > 0


def test_java_markers_inside_string(tmp_path: Path):
    """Ensure // and block-comment markers inside Java strings are ignored."""
    test_file = write_file(
        tmp_path / "Example.java",
        """
public class Example {
    String url = "https://example.com";
    String fake = "/* not comment */";
}
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 0
    assert result.ncloc == 4
    assert result.classes >= 1


def test_c_inline_comment(tmp_path: Path):
    """Ensure a C inline comment counts as ncloc, not as a comment-only line."""
    test_file = write_file(
        tmp_path / "main.c",
        """
int main() {
    int x = 0; // initialize
    return x;
}
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 0
    assert result.ncloc == 4
    assert result.statements >= 2
    assert result.functions >= 1


def test_java_block_marker_inside_string(tmp_path: Path):
    """Ensure a Java block-comment marker inside a string is ignored."""
    test_file = write_file(
        tmp_path / "Example.java",
        """
public class Example {
    String fake = "/* not a real block comment */";
    int x = 5;
}
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 0
    assert result.ncloc == 4


def test_html_comments(tmp_path: Path):
    """Count single-line and multi-line HTML comment blocks."""
    test_file = write_file(
        tmp_path / "index.html",
        """
<!-- page comment -->
<div>Hello</div>
<!--
multi-line comment
-->
<span>World</span>
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 6
    assert result.comment_lines == 4
    assert result.ncloc == 2


def test_css_comments(tmp_path: Path):
    """Count CSS block comments."""
    test_file = write_file(
        tmp_path / "style.css",
        """
/* main style */
body {
  margin: 0;
}
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 1
    assert result.ncloc == 3


def test_sql_comments(tmp_path: Path):
    """Count SQL single-line, inline, and block comments."""
    test_file = write_file(
        tmp_path / "query.sql",
        """
-- select users
SELECT * FROM users; -- inline comment
/* block comment */
SELECT * FROM orders;
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 2
    assert result.ncloc == 2
    assert result.statements >= 2


def test_shell_comments(tmp_path: Path):
    """Count Shell comments and document the current shebang approximation."""
    test_file = write_file(
        tmp_path / "script.sh",
        """
#!/bin/bash
# real comment
echo "hello # not comment"
echo done # inline comment
""",
    )

    result = analyze_file(test_file)

    assert result.lines == 4
    assert result.comment_lines == 2
    assert result.ncloc == 2


def test_yaml_comments(tmp_path: Path):
    """Ensure YAML # markers are counted only when they are outside strings."""
    test_file = write_file(
        tmp_path / "config.yml",
        """
# config comment
name: test
url: "https://example.com"
value: "# not comment"
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 1
    assert result.ncloc == 3


def test_ruby_comments(tmp_path: Path):
    """Count Ruby =begin and =end block-comment lines."""
    test_file = write_file(
        tmp_path / "example.rb",
        """
=begin
Ruby block comment
=end
x = 5
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 3
    assert result.ncloc == 1


def test_lua_comments(tmp_path: Path):
    """Count Lua single-line and multi-line comments."""
    test_file = write_file(
        tmp_path / "example.lua",
        """
-- single comment
--[[
block comment
]]
local x = 5
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 4
    assert result.ncloc == 1


def test_haskell_comments(tmp_path: Path):
    """Count Haskell single-line and block comments."""
    test_file = write_file(
        tmp_path / "Example.hs",
        """
-- single comment
{-
block comment
-}
main = putStrLn "hello"
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 4
    assert result.ncloc == 1


def test_matlab_comments(tmp_path: Path):
    """Count MATLAB single-line and block comments."""
    test_file = write_file(
        tmp_path / "example.m",
        """
% comment
%{
block comment
%}
x = 5;
""",
    )

    result = analyze_file(test_file)

    assert result.comment_lines == 4
    assert result.ncloc == 1


def test_repo_aggregation(tmp_path: Path):
    """Aggregate metrics from multiple supported source files in one repository."""
    write_file(
        tmp_path / "a.py",
        """
# comment
x = 1
""",
    )

    write_file(
        tmp_path / "b.js",
        """
// comment
const y = 2;
""",
    )

    repo_result, file_results = analyze_repository(tmp_path)

    assert repo_result.files == 2
    assert len(file_results) == 2
    assert repo_result.lines == 4
    assert repo_result.comment_lines == 2
    assert repo_result.ncloc == 2
    assert repo_result.comment_density == 50.0


def test_repo_skips_ignored_files(tmp_path: Path):
    """Skip vendor folders and binary files during repository analysis."""
    write_file(
        tmp_path / "main.py",
        """
x = 1
""",
    )

    vendor_dir = tmp_path / "node_modules"
    vendor_dir.mkdir()

    write_file(
        vendor_dir / "ignored.js",
        """
const x = 1;
""",
    )

    binary_file = tmp_path / "image.png"
    binary_file.write_bytes(b"fake image content")

    repo_result, file_results = analyze_repository(tmp_path)

    assert repo_result.files == 1
    assert len(file_results) == 1
    assert file_results[0].file_path.endswith("main.py")


def test_empty_file(tmp_path: Path):
    """Return zero metrics for an empty file."""
    test_file = tmp_path / "empty.py"
    test_file.write_text("", encoding="utf-8")

    result = analyze_file(test_file)

    assert result.lines == 0
    assert result.ncloc == 0
    assert result.comment_lines == 0
    assert result.comment_density == 0.0


def test_blank_file(tmp_path: Path):
    """Count blank physical lines without increasing ncloc or comment lines."""
    test_file = tmp_path / "blank.py"
    test_file.write_text("\n\n\n", encoding="utf-8")

    result = analyze_file(test_file)

    assert result.lines == 3
    assert result.ncloc == 0
    assert result.comment_lines == 0
    assert result.comment_density == 0.0


def test_unsupported_file(tmp_path: Path):
    """Raise ValueError when analyzing an unsupported file extension."""
    test_file = write_file(
        tmp_path / "notes.txt",
        """
hello
""",
    )

    with pytest.raises(ValueError):
        analyze_file(test_file)