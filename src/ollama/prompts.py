SIZE_METRICS_PROMPT = """You are a source-code metrics analyzer.

Analyze the extracted-files JSON below (a list of source code files from
one repository) and return REPOSITORY-LEVEL Size metrics as JSON.

INPUT JSON STRUCTURE
The input has these top-level fields:
•⁠  ⁠owner: repository owner
•⁠  ⁠repository: repository name
•⁠  ⁠default_branch: branch the snapshot is from
•⁠  ⁠file_count: number of files in the list
•⁠  ⁠files: list of {{path, extension, content}}

YOUR TASK
For each file in ⁠ files ⁠, count Lines, NCLOC, Comment Lines, Statements,
Functions, Classes. Then AGGREGATE across all files to get the repository
total.

DEFINITIONS (based on SonarQube standard):

1.⁠ ⁠files
   Total number of source code files analyzed.
   Equal to the length of ⁠ files ⁠ list.

2.⁠ ⁠lines
   Sum of physical lines across all files (count newline-separated lines).
   Include blank lines and comment lines.

3.⁠ ⁠ncloc (Non-Comment Lines of Code)
   Sum of lines that contain at least one code character across all files.
   EXCLUDE blank lines.
   EXCLUDE lines that contain only comments.
   INCLUDE lines that contain code with an inline comment after it.

4.⁠ ⁠comment_lines
   Sum of lines containing only comments OR commented-out code.
   INCLUDE lines inside multi-line / block comments / docstrings.
   EXCLUDE blank lines and pure decoration lines (e.g. **).

5.⁠ ⁠comment_density_pct
   Formula: comment_lines / (ncloc + comment_lines) * 100
   If (ncloc + comment_lines) == 0, return 0.0.

6.⁠ ⁠statements
   Sum of executable or declarative statements across all files.
   Includes assignments, function calls, returns, conditionals,
   loops, declarations, imports.

7.⁠ ⁠functions
   Sum of function or method definitions across all files.
   Language hints: Python ⁠ def ⁠, JS/TS ⁠ function ⁠ / arrow / class methods,
   Java methods, Go ⁠ func ⁠, Ruby ⁠ def ⁠, PHP ⁠ function ⁠.

8.⁠ ⁠classes
   Sum of class definitions (and interfaces, enums, annotations
   if the language has them) across all files.

RULES
•⁠  ⁠Count carefully across ALL files in the list, not just the first few.
•⁠  ⁠If a file is empty or unparseable, treat all its counts as zero.
•⁠  ⁠Output JSON ONLY. No prose, no markdown fences, no explanation about how you compute that metrics or values. ONLY SHOW OUTPUT SCHEMA
•  Do NOT SHOW the introduction explanation, for example: Here is the output JSON with repository-level size metrics: . JUST
    GIVE OUTPUT SCHEMA with no additional information

OUTPUT SCHEMA (exact keys, integers except comment_density_pct which is float):
{{
  "files": <integer>,
  "lines": <integer>,
  "ncloc": <integer>,
  "comment_lines": <integer>,
  "comment_density_pct": <float>,
  "statements": <integer>,
  "functions": <integer>,
  "classes": <integer>
}}

INPUT JSON:
{file_content_json}
"""


SIZE_METRIC_CHUNK_PROMPT = """You are a source-code metrics analyzer.

For EACH file in the chunk below, return its Size metrics as JSON.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
For each file in `files`, count Lines, NCLOC, Comment Lines, Statements,
Functions, Classes. Return ONE result per file, preserving the order
in `files`. Keep the exact `path` string from the input so the caller
can match.

DEFINITIONS (based on SonarQube standard):

1. lines
   Physical lines in the file (count newline-separated lines).
   Include blank lines and comment lines.

2. ncloc (Non-Comment Lines of Code)
   Lines with at least one code character.
   EXCLUDE blank lines.
   EXCLUDE lines that contain only comments.
   INCLUDE lines that contain code with an inline comment after it.

3. comment_lines
   Lines containing only comments OR commented-out code.
   INCLUDE lines inside multi-line / block comments / docstrings.
   EXCLUDE blank lines and pure decoration lines (e.g. ******).

4. statements
   Executable or declarative statements: assignments, function calls,
   returns, conditionals, loops, declarations, imports.

5. functions
   Function or method definitions.
   Language hints: Python `def`, JS/TS `function` / arrow / class methods,
   Java methods, Go `func`, Ruby `def`, PHP `function`.

6. classes
   Class definitions (and interfaces, enums, annotations if the
   language has them).

RULES
- Count carefully for each file.
- If a file is empty or unparseable, return zeros for that file.
- Output JSON ONLY. No prose, no markdown fences, no explanation.

OUTPUT SCHEMA (exact keys, one entry per file, preserving input order):
{{
  "files": [
    {{
      "path": "<file path>",
      "lines": <integer>,
      "ncloc": <integer>,
      "comment_lines": <integer>,
      "statements": <integer>,
      "functions": <integer>,
      "classes": <integer>
    }}
  ]
}}

REMINDER: Begin your response with `{{` and end with `}}`. NOTHING ELSE.
No prose, no markdown fences, no explanation.

INPUT JSON:
{chunk_json}
"""



# =========================
# FILES
# =========================

FILES_PROMPT = """
You are a source-code metrics analyzer.

Count how many source code files are in this chunk.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- filename_count: number of filenames in this chunk
- filenames: list of filename strings

YOUR TASK
Return the total number of entries in the `filenames` list as an integer.

DEFINITION
- files: Integer equal to the length of the `filenames` list.

RULES
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": <integer>
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# LINES
# =========================

LINES_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its physical line count.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- lines: Total physical lines in the file, equivalent to
  Python's len(content.splitlines()).
- Treat `\\n` (LF) and `\\r\\n` (CRLF) as one line break each.
- A trailing newline does NOT add an extra empty line.
- Include code lines, comment lines, and blank lines.

EXAMPLES
- ""            → 0
- "abc"         → 1
- "a\\nb\\nc"   → 3
- "a\\nb\\n"    → 2
- "\\n\\n\\n"   → 3

RULES
- Count carefully for each file.
- If a file is empty, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "lines": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# NCLOC
# =========================

NCLOC_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its NCLOC.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- ncloc: Non-comment lines of code.
- Count lines containing at least one code character.
- Exclude blank lines.
- Exclude lines containing only comments.
- Include lines containing code followed by an inline comment.

RULES
- Follow the syntax of the file's programming language.
- If a file is empty or unparseable, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "ncloc": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# COMMENT LINES
# =========================

COMMENT_LINES_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its comment-line count.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- comment_lines: Lines containing only comments or commented-out code.
- Include lines inside multi-line comments.
- Include lines inside block comments.
- Include documentation comments or docstrings used as documentation.
- Exclude blank lines.
- Exclude pure decoration lines such as repeated `*` characters.
- Do not count a code line with an inline comment as a comment-only line.

RULES
- Follow the comment syntax of the file's programming language.
- If a file is empty or unparseable, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "comment_lines": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# COMMENT DENSITY
# =========================

COMMENT_DENSITY_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its comment density.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITIONS
- ncloc: Lines containing code, excluding blank and comment-only lines.
- comment_lines: Lines containing only comments or commented-out code.
- comment_density_pct:
  comment_lines / (ncloc + comment_lines) * 100

If both ncloc and comment_lines are 0, return 0.0.

RULES
- Return the percentage rounded to two decimal places.
- If a file is empty or unparseable, return 0.0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "comment_density_pct": <number>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# STATEMENTS
# =========================

STATEMENTS_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its number of statements.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- statements: Executable or declarative statements.
- Include assignments.
- Include function or method calls.
- Include return, break, continue, and throw statements.
- Include imports and declarations.
- Include conditionals and loops.
- Follow the syntax of the file's programming language.
- Do not count comments or blank lines as statements.

RULES
- If a file is empty or unparseable, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "statements": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# FUNCTIONS
# =========================

FUNCTIONS_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its number of functions and methods.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- functions: Number of function or method definitions.
- Python: count `def` and `async def`.
- JavaScript/TypeScript: count functions, arrow functions assigned as
  callable definitions, and class/object methods.
- Java/C#/C++: count method and function definitions.
- Go: count `func` definitions.
- Ruby: count `def`.
- PHP: count `function`.
- Do not count function calls.

RULES
- Follow the syntax of the file's programming language.
- If a file is empty or unparseable, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "functions": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""


# =========================
# CLASSES
# =========================

CLASSES_PROMPT = """
You are a source-code metrics analyzer.

For EACH file in the chunk below, calculate its number of classes.

INPUT JSON STRUCTURE
- chunk_index: which chunk this is (informational only)
- file_count: number of files in this chunk
- files: list of {{path, extension, content}}

YOUR TASK
Return ONE result per input file, preserving the original order.
Keep the exact `path` value from the input.

DEFINITION
- classes: Number of class-like type definitions.
- Count class definitions.
- Count interfaces.
- Count enums.
- Count annotations when the language supports annotation declarations.
- Do not count object instances or constructor calls.

RULES
- Follow the syntax of the file's programming language.
- If a file is empty or unparseable, return 0.
- Output JSON ONLY.
- Do not include prose, markdown fences, or explanations.

OUTPUT SCHEMA:
{{
  "files": [
    {{
      "path": "<file path>",
      "classes": <integer>
    }}
  ]
}}

Begin your response with `{{` and end with `}}`. NOTHING ELSE.

INPUT JSON:
{chunk_json}
"""