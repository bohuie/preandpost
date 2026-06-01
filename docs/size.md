# Size
The implementation analyzes supported source files using line-based scanning and generates both file-level and repository-level summaries.

The following metrics are included:

- **Files**: The number of files.
- **Lines**: The number of physical lines, number of carriage returns.
- **Lines of Code (`ncloc`)**: The number of physical lines that contain at least one character which is neither a whitespace nor a tabulation nor part of a comment.
- **Comment Lines**: The number of lines containing either comment or commented-out code.
- **Comment Density**: The `comment lines density = comment lines / (lines of code + comment lines) * 100`.
- **Statements**: The number of statements, e.g., `x = 5; y = 10; print(x + y)` which has 3 statements.
- **Functions**: The number of functions. Depending on the language, a function is defined as either a function or a method.
- **Classes**: The number of classes, including nested classes, interfaces, enums, and annotations.

## Folder Structure
```bash
Folder Structure
preandpost/
├── src/
│   └── metrics/
│       └── size.py                 # Size metric extraction logic
├── scripts/
│   └── run_size.py                 # Run Size metric extraction
└── tests/
│   └── test_size.py                # Unit tests
└── data/
    └── outputs/                     # Generated outputs 
        └── size/
            ├── files_summary.csv    # File-level metrics
            └── repos_summary.csv    # Repository-level metrics
```

## Workflow
``` bash
Repository path
    ↓
Scan repository recursively
    ↓
Filter files and folders
    ├── Skip ignored folders
    │   e.g. .git, node_modules, vendor, build, dist, coverage, .venv
    ├── Skip binary or unsupported files
    │   e.g. .png, .jpg, .pdf, .zip, .class, .jar
    └── Keep supported source files
    ↓
For each supported source file
    ↓
Detect programming language from file extension
    ↓
Detect comment style from file extension
    ├── Python      → # and triple quotes
    ├── Java / JS   → // and /* */
    ├── SQL         → --, #, and /* */
    └── HTML        → <!-- -->
    ↓
Initialize file-level counters
    ├── lines = 0
    ├── comment_lines = 0
    ├── ncloc = 0
    ├── statements = 0
    ├── functions = 0
    └── classes = 0
    ↓
Read file line by line
    ↓
Count every physical line
    └── lines += 1
    ↓
Check line type
    ├── Blank line
    │   └── Skip remaining checks
    │
    ├── Inside multi-line block comment
    │   ├── comment_lines += 1
    │   ├── Check whether block comment ends
    │   └── If code remains after the block:
    │       ├── ncloc += 1
    │       └── Count statements, functions, and classes
    │
    ├── New block comment found
    │   ├── Hide strings first
    │   ├── comment_lines += 1
    │   ├── Find matching end marker
    │   ├── If block ends on the same line:
    │   │   └── Analyze remaining code before and after the block
    │   └── If block continues:
    │       └── Store block-comment state for the next line
    │
    ├── Single-line or inline comment found
    │   ├── Hide strings first
    │   ├── If no code appears before the marker:
    │   │   └── comment_lines += 1
    │   └── If code appears before the marker:
    │       ├── ncloc += 1
    │       └── Count statements, functions, and classes
    │
    └── Ordinary code line
        ├── ncloc += 1
        └── Count statements, functions, and classes
    ↓
Calculate file-level comment density
    └── comment_lines / (ncloc + comment_lines) × 100
    ↓
Add file-level metrics to repository totals
    ↓
Repeat for all supported source files
    ↓
Calculate repository-level comment density
    └── repo_comment_lines / (repo_ncloc + repo_comment_lines) × 100
    ↓
Return results
    ├── files
    ├── lines
    ├── comment_lines
    ├── ncloc
    ├── comment_density
    ├── statements
    ├── functions
    └── classes
```

## Pseudocode
```bash
INPUT:
    repository_path

OUTPUT:
    files
    lines
    comment_lines
    ncloc
    comment_density
    statements
    functions
    classes


------------------------------------------------------------
1. FILTER FILES
------------------------------------------------------------

source_files = []

for each file in repository recursively:

    if file is inside skipped folder:
        skip file
        # e.g. .git, node_modules, vendor, build, dist, coverage, .venv

    if file extension is binary or unsupported:
        skip file
        # e.g. .png, .jpg, .pdf, .zip, .class, .jar

    if file extension is supported source code:
        add file to source_files


------------------------------------------------------------
2. INITIALIZE REPOSITORY METRICS
------------------------------------------------------------

repo_files = 0
repo_lines = 0
repo_comment_lines = 0
repo_ncloc = 0
repo_statements = 0
repo_functions = 0
repo_classes = 0


------------------------------------------------------------
3. ANALYZE EACH FILE
------------------------------------------------------------

for each file in source_files:

    detect programming language from file extension
    detect comment style from file extension

    # Examples:
    # Python      → single: #        block: """ """
    # Java / JS   → single: //       block: /* */
    # SQL         → single: --, #    block: /* */
    # HTML        → block: <!-- -->

    initialize:
        file_lines = 0
        file_comment_lines = 0
        file_ncloc = 0
        file_statements = 0
        file_functions = 0
        file_classes = 0

        in_block_comment = False
        block_end_marker = None


    --------------------------------------------------------
    3A. PROCESS EACH LINE
    --------------------------------------------------------

    for each line in file:

        file_lines += 1

        if line is blank:
            continue


        ----------------------------------------------------
        CASE 1: ALREADY INSIDE MULTI-LINE BLOCK COMMENT
        ----------------------------------------------------

        if in_block_comment:

            file_comment_lines += 1

            if block_end_marker exists in line:
                in_block_comment = False
                block_end_marker = None

                code_after_block = text after block_end_marker

                if code_after_block contains real code:
                    file_ncloc += 1
                    count statements/functions/classes from code_after_block

            continue


        ----------------------------------------------------
        CASE 2: FIND NEW BLOCK COMMENT
        ----------------------------------------------------

        masked_line = hide strings in line
        # Example:
        # url = "https://example.com"
        # becomes:
        # url = "                   "

        block_start = find first block-comment marker in masked_line

        if block_start is found:

            file_comment_lines += 1

            matching_end_marker = get matching block end marker

            code_before_block = text before block start marker
            code_after_start = text after block start marker

            if matching_end_marker is found in same line:

                code_after_block = text after block end marker

                remaining_code =
                    code_before_block + code_after_block

                remove inline comment from remaining_code

                if remaining_code contains real code:
                    file_ncloc += 1
                    count statements/functions/classes from remaining_code

            else:

                in_block_comment = True
                block_end_marker = matching_end_marker

                if code_before_block contains real code:
                    file_ncloc += 1
                    count statements/functions/classes from code_before_block

            continue


        ----------------------------------------------------
        CASE 3: FIND SINGLE-LINE OR INLINE COMMENT
        ----------------------------------------------------

        masked_line = hide strings in line
        single_comment = find first single-line marker in masked_line

        if single_comment is found: (e.g., //)

            code_before_comment = text before comment marker

            if code_before_comment is empty or whitespace only:
                file_comment_lines += 1

            else:
                file_ncloc += 1
                count statements/functions/classes from code_before_comment

            continue


        ----------------------------------------------------
        CASE 4: ORDINARY CODE LINE
        ----------------------------------------------------

        file_ncloc += 1
        count statements/functions/classes from line


    --------------------------------------------------------
    3B. CALCULATE FILE COMMENT DENSITY
    --------------------------------------------------------

    denominator = file_ncloc + file_comment_lines

    if denominator > 0:
        file_comment_density =
            file_comment_lines / denominator * 100
    else:
        file_comment_density = 0


    --------------------------------------------------------
    3C. ADD FILE METRICS TO REPOSITORY TOTAL
    --------------------------------------------------------

    repo_files += 1
    repo_lines += file_lines
    repo_comment_lines += file_comment_lines
    repo_ncloc += file_ncloc
    repo_statements += file_statements
    repo_functions += file_functions
    repo_classes += file_classes


------------------------------------------------------------
4. COUNT STATEMENTS
------------------------------------------------------------

function count_statements(clean_line, language):

    masked_line = hide strings in clean_line

    if masked_line is empty:
        return 0

    if language is Python:

        if line is a block header ending with ":":
            return 0
            # e.g. if, for, while, def, class, try

        return number of semicolons + 1

        # x = 5
        # → 1 statement

        # x = 5; y = 10
        # → 2 statements

    semicolon_count = number of semicolons in masked_line

    if semicolon_count > 0:
        return semicolon_count

    if language commonly omits semicolons:
        return 1
        # e.g. Go, Ruby, R, Shell

    return 0


------------------------------------------------------------
5. COUNT FUNCTIONS
------------------------------------------------------------

function count_functions(clean_line, language):

    masked_line = hide strings in clean_line

    choose regex patterns based on language:
        Python                  → def, async def
        JavaScript / TypeScript → function, arrow function, method
        C-style                 → return type + name + (...) + {

    if line starts with control-flow keyword:
        return 0
        # e.g. if, for, while, switch, catch

    for each function pattern:

        if masked_line matches pattern:
            return 1

    return 0


------------------------------------------------------------
6. COUNT CLASSES
------------------------------------------------------------

function count_classes(clean_line, language):

    masked_line = hide strings in clean_line

    choose regex patterns based on language:
        Python                  → class
        JavaScript / TypeScript → class, interface, enum
        C-style                 → class, interface, enum, struct

    for each class pattern:

        if masked_line matches pattern:
            return 1

    return 0


------------------------------------------------------------
7. CALCULATE REPOSITORY COMMENT DENSITY
------------------------------------------------------------

denominator = repo_ncloc + repo_comment_lines

if denominator > 0:
    repo_comment_density =
        repo_comment_lines / denominator * 100
else:
    repo_comment_density = 0


------------------------------------------------------------
8. RETURN RESULTS
------------------------------------------------------------

return:
    files = repo_files
    lines = repo_lines
    comment_lines = repo_comment_lines
    ncloc = repo_ncloc
    comment_density = repo_comment_density
    statements = repo_statements
    functions = repo_functions
    classes = repo_classes

```

## Files

### `src/metrics/size.py`

Contains the main Size metric logic.

The scanner:

- Filters unsupported files and ignored folders, such as binary files, build folders, vendor folders, and `node_modules`;
- Detects the programming language and comment syntax based on file extension;
- Masks string contents (Replaces string contents with space) before searching for comment markers, e.g., `#`;
- Tracks multi-line block comments;
- Computes metrics for each supported source file;
- Aggregates file-level metrics into repository-level results.

### `scripts/run_size.py`

Runs Size metric extraction on the configured cloned repositories.

Generated outputs:

```text
data/outputs/size/files_summary.csv
data/outputs/size/repos_summary.csv
```

### `tests/test_size.py`

Adds unit tests for:

- Various programming language comment styles;
- String masking;
- Inline and multi-line comments;
- Escaped quotes;
- `ncloc`;
- Statement, function, and class detection;
- Repository-level aggregation;
- Skipped folders and unsupported files;
- Empty and blank-only files.

## Metric Computation

| Metric | Computation |
|---|---|
| Files | Number of supported source files analyzed |
| Lines | Number of physical lines, including blank and comment lines |
| Comment Lines | Number of comment-only lines and block-comment lines |
| Lines of Code (`ncloc`) | Number of physical lines containing active code |
| Comment Density | `comment_lines / (ncloc + comment_lines) * 100` |
| Statements | Count based on executable lines or semicolons, depending on the language |
| Functions | Count using language-specific regex patterns |
| Classes | Count of class declarations using language-specific regex patterns |

## Notes

- Inline comments are treated as code lines.
For example: 
```bash
x = 7  # initialize the value
```
Output:
```bash
ncloc = 1
comment_lines = 0
```

- A line containing both a block comment and active code can contribute to both `comment_lines` and `ncloc`.
For example:
```bash
x = 7; '''initialize the value'''
```
Output:
```bash
ncloc = 1
comment_lines = 1
```

- Statement, function, and class detection use line-based scanning.

## Limitation
This implementation uses a line-based approximation. Some metrics may not be detected perfectly because programming languages have different syntax formats and language-specific constructs.

## How to Run

Run the unit tests:

```bash
PYTHONPATH=. python -m pytest tests/test_size.py -v
```

Run the script:

```bash
PYTHONPATH=. python scripts/run_size.py
```

# Metric Size Calculation
## Filtering Folder and File
```bash
Input: repository_path

function should_skip_folder(folder_path):

    folder_name = lowercase(folder_path.name)

    if folder_name is in SKIP_DIRS:
        return True

    return False

function should_skip_file(file_path):

    extension = lowercase(file extension)

    if extension is in SKIP_FILE_EXTENSIONS:
        return True

    if extension is not in SOURCE_EXTENSIONS:
        return True

    for each folder_name in file_path parent folders:
        if lowercase(folder_name) is in SKIP_DIRS:
            return True

    return False

function collect_source_files(repository_path):

    init:
        source_files = empty list

    for each item inside repository_path recursively:

        if item is a folder:
            if should_skip_folder(item):
                do not enter this folder
                continue

        if item is a file:
            if should_skip_file(item):
                continue

            add item to source_files

    return source_files
```

## Comment Lines
```bash
For each file:

    if file should be skipped:
        skip file

    detect comment style based on file extension

    init:
        comment_lines = 0
        in_block_comment = False
        block_end_marker = None

    for each line in file:

        if line is blank:
            continue

        # CASE 1: Scanner is already inside a multi-line block comment
        if in_block_comment:

            comment_lines += 1

            if block_end_marker exists in line:
                in_block_comment = False
                block_end_marker = None

            continue

        # CASE 2: Line starts or contains a block comment marker
        block_start = find first block comment marker outside strings

        if block_start is found:

            comment_lines += 1

            matching_end_marker = get matching block end marker

            if matching_end_marker is not found after block_start in the same line:
                in_block_comment = True
                block_end_marker = matching_end_marker

            continue

        # CASE 3: Check single-line comment marker
        masked_line = hide strings in line
        single_comment = find first single-line comment marker in masked_line

        if single_comment is found:

            code_before_comment = text before comment marker

            if code_before_comment is empty or whitespace only:
                comment_lines += 1

            # Inline comments are not counted as comment_lines
            # Example: x = 5  # explanation
            continue

    return comment_lines
```

## Lines of Code/ncloc
```bash
For each file:

    if file should be skipped:
        skip file

    detect comment style based on file extension

    init:
        ncloc = 0
        in_block_comment = False
        block_end_marker = None

    for each line in file:

        if line is blank:
            continue

        # CASE 1: currently inside a multi-line block comment
        if in_block_comment:

            if block_end_marker is not found in line:
                # Entire line is still part of the comment
                continue

            # Block comment ends on this line
            in_block_comment = False
            block_end_marker = None

            text_after_block = text after block_end_marker
            text_after_block = remove inline comment from text_after_block

            if text_after_block contains real code:
                ncloc += 1

            continue

        # CASE 2: Detect a new block comment
        block_start = find first block comment marker outside strings

        if block_start is found:

            code_before_block = text before block start marker
            text_after_start = text after block start marker
            matching_end_marker = corresponding block end marker

            if matching_end_marker is found in the same line:

                code_after_block = text after block end marker
                remaining_code = code_before_block + code_after_block
                remaining_code = remove inline comment from remaining_code

                if remaining_code contains real code:
                    ncloc += 1

            else:
                # Comment continues onto the next line
                in_block_comment = True
                block_end_marker = matching_end_marker

                code_before_block = remove inline comment from code_before_block

                if code_before_block contains real code:
                    ncloc += 1

            continue

        # CASE 3: Detect single-line or inline comments
        masked_line = hide strings in line
        single_comment = find first single-line comment marker in masked_line

        if single_comment is found:

            code_before_comment = text before comment marker

            if code_before_comment contains real code:
                # Example: x = 5  # explanation
                ncloc += 1

            # If there is no code before marker, line is comment-only
            continue

        # CASE 4: Ordinary code line
        if line contains real code:
            ncloc += 1

    return ncloc
```

## Functions
```bash
For each file:

    if file should be skipped:
        skip file

    detect programming language based on file extension
    detect comment style based on file extension
    choose function regex patterns based on language:
        Python                  → Python function patterns
        JavaScript / TypeScript → JavaScript function patterns
        Java / C / C++ / C#     → C-style function patterns

    init:
        functions = 0
        in_block_comment = False
        block_end_marker = None

    for each line in file:

        if line is blank:
            continue

        # STEP 1: Remove comments and keep only the remaining code
        clean_line = remove comment content from line
                     while tracking multi-line block-comment state

        if clean_line is empty or whitespace only:
            continue

        # STEP 2: Hide strings
        masked_line = hide strings in clean_line

        # Example:
        # message = "function fakeFunction() {"
        # becomes:
        # message = "                         "

        # STEP 3: Ignore control-flow lines
        if masked_line starts with a control-flow keyword:
            continue

        # Example:
        # if (x > 0) {
        # while (count < 10) {
        # for (int i = 0; i < 10; i++) {
        #
        # These lines may look similar to functions,
        # but they must not be counted.

        # STEP 4: Check function patterns for the detected language
        for each function_pattern in selected function regex patterns:

            if masked_line matches function_pattern:
                functions += 1

                # Stop checking other patterns for the same line
                # because one line should count as at most one function.
                break

    return functions
```

## Classes
```bash
For each file:

    if file should be skipped:
        skip file

    detect programming language based on file extension
    detect comment style based on file extension
    choose class regex patterns based on language:
        Python                  → Python class patterns
        JavaScript / TypeScript → JavaScript class/interface/enum patterns
        Java / C / C++ / C#     → C-style class/interface/enum/struct patterns

    init:
        classes = 0
        in_block_comment = False
        block_end_marker = None

    for each line in file:

        if line is blank:
            continue

        # STEP 1: Remove comments and keep only remaining code
        clean_line = remove comment content from line
                     while tracking multi-line block-comment state

        if clean_line is empty or whitespace only:
            continue

        # STEP 2: Hide strings so class-like text inside strings is ignored
        masked_line = hide strings in clean_line

        # Example:
        # message = "class FakeClass {"
        # becomes:
        # message = "                 "

        # STEP 3: Check class-like patterns for the detected language
        for each class_pattern in selected class regex patterns:

            if masked_line matches class_pattern:
                classes += 1

                # Stop checking other patterns for the same line
                # because one line should count as at most one class-like declaration.
                break

    return classes
```

## Statements
```bash
For each file:

    if file should be skipped:
        skip file

    detect programming language based on file extension
    detect comment style based on file extension

    init:
        statements = 0
        in_block_comment = False
        block_end_marker = None

    for each line in file:

        if line is blank:
            continue

        # STEP 1: Remove comments and keep only the remaining code
        clean_line = remove comment content from line
                     while tracking multi-line block-comment state

        if clean_line is empty or whitespace only:
            continue

        # STEP 2: Hide strings 
        masked_line = hide strings in clean_line

        # Example:
        # message = "hello; world"
        # becomes:
        # message = "            "

        if masked_line is empty or whitespace only:
            continue

        # STEP 3: Count Python statements
        if language is Python:

            first_token = get first token from masked_line

            if masked_line ends with ":"
               and first_token is a Python block header:
                continue

                # Example:
                # if x > 0:
                # for item in items:
                # def hello():
                # class Student:
                #
                # These lines open a block and are not counted
                # as executable statements in this approximation.

            statements += number of semicolons in masked_line + 1

            # Example:
            # x = 5
            # → 1 statement
            #
            # x = 5; y = 10
            # → 2 statements

            continue

        # STEP 4: Count C-style statements
        semicolon_count = number of semicolons in masked_line

        if semicolon_count > 0:
            statements += semicolon_count
            continue

            # Example:
            # int x = 5;
            # → 1 statement
            #
            # int x = 5; int y = 10;
            # → 2 statements

        # STEP 5: Count statements for languages that commonly omit semicolons
        if language is Go, Ruby, R, Shell, YAML, or TOML:
            statements += 1
            continue

        # STEP 6: Otherwise, do not add any statement

    return statements
```

## Comments (%) / Comment Density
```bash
For each file:

    initialize:
        comment_lines = 0
        ncloc = 0

    for each line in file:

        if line is blank:
            continue

        remove comment content while preserving any remaining code

        if line is a comment-only line:
            comment_lines += 1
            continue

        if line contains a block comment:
            comment_lines += 1

            if remaining code exists before or after the block comment:
                ncloc += 1

            continue

        if line contains active code:
            ncloc += 1

            # Inline comments are not counted separately as comment lines.
            # Example:
            # x = 5  # explanation
            #
            # This line contributes:
            # ncloc += 1
            # comment_lines += 0


    denominator = ncloc + comment_lines

    if denominator > 0:
        comment_density =
            comment_lines / denominator * 100
    else:
        comment_density = 0

    return comment_density
```

## Lines
```bash
For each file:

    initialize:
        lines = 0

    read file line by line

    for each line in file:

        lines += 1

        # Count every physical line, including:
        # - code lines
        # - comment lines
        # - blank lines

    return lines
```

## Files
```bash
For each repository:

    initialize:
        files = 0

    scan repository recursively

    for each discovered file:

        if file is inside an ignored folder:
            skip file
            # e.g. .git, node_modules, vendor, build, dist, coverage, .venv

        if file extension is binary or unsupported:
            skip file
            # e.g. .png, .jpg, .pdf, .zip, .class, .jar

        if file extension is supported source code:
            files += 1

    return files
```