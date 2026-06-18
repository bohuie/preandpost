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
