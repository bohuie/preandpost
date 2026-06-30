# =========================
# FILE COUNT
# =========================

FILES_PROMPT = """
You are a deterministic source-file counter.

The input contains one batch of source-code file paths.

INPUT JSON STRUCTURE
- chunk_index: batch position, informational only
- path_count: number of path entries in this batch
- paths: list of complete source-file path strings

TASK
Count the number of entries in the `paths` JSON array.

RULES
1. Each string in `paths` represents exactly one source-code file.
2. Count every entry, even if two paths have the same filename.
3. Do not inspect or interpret the path strings.
4. Do not count folders separately.
5. Do not remove duplicates.
6. The result must equal the number of elements in `paths`.
7. If `paths` is empty, return 0.
8. Return valid JSON only.
9. Do not include prose, markdown fences, comments, or explanations.

OUTPUT SCHEMA
{{
  "files": <non-negative integer>
}}

Begin with `{{` and end with `}}`.

INPUT JSON:
{chunk_json}
"""


# =========================
# LINES
# =========================

LINES_PROMPT = """
You are a deterministic source-code chunk line counter.

Each input chunk contains a `physical_lines` array.

Every object in `physical_lines` represents exactly one physical line.
Each object contains:

- `line_number`: the line's sequential position within the current chunk
- `text`: the source-code text on that physical line

The numbering starts at 1 for every chunk and increases sequentially
without gaps.

TASK

For each chunk:

1. If `physical_lines` is empty, return `lines` as 0.

2. Otherwise, find the largest `line_number` in `physical_lines`.

3. Return that largest `line_number` as `lines`.

Do not count source-code statements.
Do not classify code, comments, or blank lines.
Do not count newline characters.
Do not count array punctuation.
Do not add 1 to the largest line number.
Do not subtract 1 from the largest line number.

The `text` value is informational only.
A line whose `text` is empty or whitespace-only is still represented by
its own `line_number`.

EXAMPLES

Input physical lines:

[
  {{"line_number": 1, "text": "code"}},
  {{"line_number": 2, "text": ""}},
  {{"line_number": 3, "text": "// comment"}}
]

The largest `line_number` is 3.
Therefore, return:

{{
  "lines": 3
}}

If the last object has:

{{
  "line_number": 57,
  "text": "?>"
}}

return exactly 57, not 56 and not 58.

VALIDATION

- Return exactly one result for each input chunk.
- Preserve the input order.
- Preserve `path` exactly.
- Preserve `file_chunk_index` exactly.
- `lines` must equal the maximum `line_number`.
- Never infer the answer from the source-code content.

OUTPUT RULES

- Return valid JSON only.
- No prose.
- No markdown fences.
- No explanations.
- Begin with `{{` and end with `}}`.

OUTPUT SCHEMA

{{
  "chunks": [
    {{
      "path": "<exact input path>",
      "file_chunk_index": <integer>,
      "lines": <integer>
    }}
  ]
}}

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