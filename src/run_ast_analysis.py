import json
import sys
import traceback
from pathlib import Path

try:
    from tree_sitter_language_pack import get_parser
except ImportError as e:
    print(f"FATAL: tree-sitter-language-pack belum diinstall.\n"
          f"  Run: pip install tree-sitter-language-pack\n"
          f"  Error: {e}")
    sys.exit(1)


sys.setrecursionlimit(20_000)


SOURCE_JSON  = (
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data/"
    "UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/"
    "project-1-crm-for-non-profits-trellis-crm.json"
)

CHUNK_LINES = 250


EXT_TO_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".sql": "sql",
    ".vue": "vue",
    ".svelte": "svelte",
}


COMMENT_TYPES = {
    "python":     {"comment"},
    "javascript": {"comment"},
    "typescript": {"comment"},
    "tsx":        {"comment"},
    "java":       {"line_comment", "block_comment"},
    "kotlin":     {"line_comment", "multiline_comment"},
    "scala":      {"comment", "block_comment"},
    "c":          {"comment"},
    "cpp":        {"comment"},
    "csharp":     {"comment"},
    "go":         {"comment"},
    "rust":       {"line_comment", "block_comment"},
    "ruby":       {"comment"},
    "php":        {"comment"},
    "swift":      {"comment", "multiline_comment"},
    "bash":       {"comment"},
    "html":       {"comment"},
    "css":        {"comment"},
    "scss":       {"comment"},
    "sql":        {"comment", "marginalia"},
    "vue":        {"comment"},
    "svelte":     {"comment"},
}


CLASS_TYPES = {
    "python":     {"class_definition"},
    "javascript": {"class_declaration"},
    "typescript": {"class_declaration", "interface_declaration",
                   "enum_declaration", "type_alias_declaration"},
    "tsx":        {"class_declaration", "interface_declaration",
                   "enum_declaration", "type_alias_declaration"},
    "java":       {"class_declaration", "interface_declaration",
                   "enum_declaration", "annotation_type_declaration"},
    "kotlin":     {"class_declaration", "object_declaration"},
    "scala":      {"class_definition", "object_definition", "trait_definition"},
    "c":          {"struct_specifier", "union_specifier", "enum_specifier"},
    "cpp":        {"class_specifier", "struct_specifier",
                   "union_specifier", "enum_specifier"},
    "csharp":     {"class_declaration", "interface_declaration",
                   "struct_declaration", "enum_declaration",
                   "record_declaration"},
    "go":         {"type_declaration"},
    "rust":       {"struct_item", "enum_item", "trait_item",
                   "impl_item", "union_item"},
    "ruby":       {"class", "module"},
    "php":        {"class_declaration", "interface_declaration",
                   "trait_declaration", "enum_declaration"},
    "swift":      {"class_declaration", "protocol_declaration",
                   "struct_declaration", "enum_declaration"},
}


CLASS_KIND = {
    "class_definition": "class",
    "class_declaration": "class",
    "interface_declaration": "interface",
    "enum_declaration": "enum",
    "annotation_type_declaration": "annotation",
    "type_alias_declaration": "type",
    "struct_declaration": "struct",
    "record_declaration": "record",
    "trait_declaration": "trait",
    "type_declaration": "type",
    "struct_item": "struct",
    "enum_item": "enum",
    "trait_item": "trait",
    "impl_item": "impl",
    "union_item": "union",
    "union_specifier": "union",
    "struct_specifier": "struct",
    "enum_specifier": "enum",
    "class_specifier": "class",
    "object_declaration": "object",
    "object_definition": "object",
    "trait_definition": "trait",
    "protocol_declaration": "protocol",
    "class": "class",
    "module": "module",
}


FUNCTION_TYPES = {
    "python":     {"function_definition"},
    "javascript": {"function_declaration", "function_expression",
                   "method_definition", "generator_function_declaration"},
    "typescript": {"function_declaration", "function_expression",
                   "method_definition", "method_signature",
                   "function_signature", "abstract_method_signature"},
    "tsx":        {"function_declaration", "function_expression",
                   "method_definition", "method_signature",
                   "function_signature", "abstract_method_signature"},
    "java":       {"method_declaration", "constructor_declaration"},
    "kotlin":     {"function_declaration"},
    "scala":      {"function_definition", "function_declaration"},
    "c":          {"function_definition"},
    "cpp":        {"function_definition"},
    "csharp":     {"method_declaration", "constructor_declaration",
                   "destructor_declaration", "local_function_statement"},
    "go":         {"function_declaration", "method_declaration"},
    "rust":       {"function_item"},
    "ruby":       {"method", "singleton_method"},
    "php":        {"function_definition", "method_declaration"},
    "swift":      {"function_declaration", "init_declaration",
                   "deinit_declaration"},
    "bash":       {"function_definition"},
}


EVENT_MAP = {
    "python": {
        "if_statement": "if",
        "elif_clause": "elif",
        "else_clause": "else",
        "for_statement": "for",
        "while_statement": "while",
        "try_statement": "try",
        "except_clause": "catch",
        "finally_clause": "finally",
        "return_statement": "return",
        "raise_statement": "throw",
        "break_statement": "break",
        "continue_statement": "continue",
        "import_statement": "import",
        "import_from_statement": "import",
        "with_statement": "with",
        "yield": "yield",
        "await": "await",
        "lambda": "lambda",
        "assert_statement": "assert",
    },
    "javascript": {
        "if_statement": "if",
        "else_clause": "else",
        "for_statement": "for",
        "for_in_statement": "for",
        "for_of_statement": "for",
        "while_statement": "while",
        "do_statement": "do_while",
        "switch_statement": "switch",
        "switch_case": "case",
        "try_statement": "try",
        "catch_clause": "catch",
        "finally_clause": "finally",
        "return_statement": "return",
        "throw_statement": "throw",
        "break_statement": "break",
        "continue_statement": "continue",
        "import_statement": "import",
        "yield_expression": "yield",
        "await_expression": "await",
        "ternary_expression": "ternary",
    },
    "java": {
        "if_statement": "if",
        "for_statement": "for",
        "enhanced_for_statement": "for",
        "while_statement": "while",
        "do_statement": "do_while",
        "switch_statement": "switch",
        "switch_expression": "switch",
        "try_statement": "try",
        "catch_clause": "catch",
        "finally_clause": "finally",
        "return_statement": "return",
        "throw_statement": "throw",
        "break_statement": "break",
        "continue_statement": "continue",
        "import_declaration": "import",
        "ternary_expression": "ternary",
    },
    "go": {
        "if_statement": "if",
        "for_statement": "for",
        "expression_switch_statement": "switch",
        "type_switch_statement": "switch",
        "select_statement": "select",
        "return_statement": "return",
        "break_statement": "break",
        "continue_statement": "continue",
        "import_declaration": "import",
        "defer_statement": "defer",
        "go_statement": "go",
    },
    "ruby": {
        "if": "if",
        "elsif": "elif",
        "else": "else",
        "unless": "unless",
        "for": "for",
        "while": "while",
        "until": "until",
        "case": "switch",
        "begin": "try",
        "rescue": "catch",
        "ensure": "finally",
        "return": "return",
        "yield": "yield",
        "break": "break",
        "next": "continue",
    },
    "php": {
        "if_statement": "if",
        "for_statement": "for",
        "foreach_statement": "for",
        "while_statement": "while",
        "do_statement": "do_while",
        "switch_statement": "switch",
        "try_statement": "try",
        "catch_clause": "catch",
        "finally_clause": "finally",
        "return_statement": "return",
        "throw_statement": "throw",
        "break_statement": "break",
        "continue_statement": "continue",
        "use_declaration": "import",
        "namespace_use_declaration": "import",
    },
    "csharp": {
        "if_statement": "if",
        "for_statement": "for",
        "foreach_statement": "for",
        "while_statement": "while",
        "do_statement": "do_while",
        "switch_statement": "switch",
        "try_statement": "try",
        "catch_clause": "catch",
        "finally_clause": "finally",
        "return_statement": "return",
        "throw_statement": "throw",
        "throw_expression": "throw",
        "break_statement": "break",
        "continue_statement": "continue",
        "using_directive": "import",
        "yield_statement": "yield",
        "await_expression": "await",
    },
    "rust": {
        "if_expression": "if",
        "for_expression": "for",
        "while_expression": "while",
        "loop_expression": "loop",
        "match_expression": "switch",
        "return_expression": "return",
        "break_expression": "break",
        "continue_expression": "continue",
        "use_declaration": "import",
    },
    "kotlin": {
        "if_expression": "if",
        "for_statement": "for",
        "while_statement": "while",
        "do_while_statement": "do_while",
        "when_expression": "switch",
        "try_expression": "try",
        "catch_block": "catch",
        "finally_block": "finally",
        "jump_expression": "return",
        "import_header": "import",
    },
}

EVENT_MAP["typescript"] = EVENT_MAP["javascript"]
EVENT_MAP["tsx"] = EVENT_MAP["javascript"]
EVENT_MAP["c"] = {
    "if_statement": "if",
    "for_statement": "for",
    "while_statement": "while",
    "do_statement": "do_while",
    "switch_statement": "switch",
    "return_statement": "return",
    "break_statement": "break",
    "continue_statement": "continue",
    "preproc_include": "import",
    "goto_statement": "goto",
}
EVENT_MAP["cpp"] = {
    **EVENT_MAP["c"],
    "try_statement": "try",
    "catch_clause": "catch",
    "throw_statement": "throw",
}


BINARY_OP_CFG = {
    "python":     ("boolean_operator", {"or": "logical_or", "and": "logical_and"}),
    "javascript": ("binary_expression", {"||": "logical_or", "&&": "logical_and",
                                          "??": "nullish_coalescing"}),
    "typescript": ("binary_expression", {"||": "logical_or", "&&": "logical_and",
                                          "??": "nullish_coalescing"}),
    "tsx":        ("binary_expression", {"||": "logical_or", "&&": "logical_and",
                                          "??": "nullish_coalescing"}),
    "java":       ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
    "go":         ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
    "csharp":     ("binary_expression", {"||": "logical_or", "&&": "logical_and",
                                          "??": "nullish_coalescing"}),
    "c":          ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
    "cpp":        ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
    "php":        ("binary_expression", {"||": "logical_or", "&&": "logical_and",
                                          "or": "logical_or", "and": "logical_and",
                                          "??": "nullish_coalescing"}),
    "ruby":       ("binary", {"||": "logical_or", "&&": "logical_and",
                              "or": "logical_or", "and": "logical_and"}),
    "rust":       ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
    "kotlin":     ("disjunction_expression", {"||": "logical_or"}),
    "swift":      ("binary_expression", {"||": "logical_or", "&&": "logical_and"}),
}


TERNARY_NODES = {
    "python": "conditional_expression",
    "javascript": "ternary_expression",
    "typescript": "ternary_expression",
    "tsx": "ternary_expression",
    "java": "ternary_expression",
    "csharp": "conditional_expression",
    "c": "conditional_expression",
    "cpp": "conditional_expression",
    "php": "conditional_expression",
}


_parser_cache = {}


def get_cached_parser(lang_name):
    if lang_name not in _parser_cache:
        _parser_cache[lang_name] = get_parser(lang_name)
    return _parser_cache[lang_name]


def safe_decode(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _read_attr(obj, *names, default=None):
    """Read a property or zero-argument method across Tree-sitter API versions."""
    for name in names:
        if not hasattr(obj, name):
            continue
        value = getattr(obj, name)
        return value() if callable(value) else value
    return default


def node_type(node):
    """Return the grammar node type across Tree-sitter API versions."""
    value = _read_attr(node, "type", "kind", "grammar_name")
    if value is None:
        available = [name for name in dir(node) if not name.startswith("_")]
        raise AttributeError(
            "Unsupported Tree-sitter Node API: no type/kind attribute. "
            f"Available attributes: {available}"
        )
    return str(value)


def _point_to_tuple(point):
    """Normalize a Tree-sitter point to (row, column)."""
    if point is None:
        raise AttributeError("Tree-sitter node point is missing.")

    if isinstance(point, (tuple, list)) and len(point) >= 2:
        return int(point[0]), int(point[1])

    row = _read_attr(point, "row")
    column = _read_attr(point, "column", "col")
    if row is not None and column is not None:
        return int(row), int(column)

    try:
        return int(point[0]), int(point[1])
    except Exception as error:
        raise TypeError(f"Unsupported point object: {point!r}") from error


def node_start_point(node):
    return _point_to_tuple(
        _read_attr(node, "start_point", "start_position")
    )


def node_end_point(node):
    return _point_to_tuple(
        _read_attr(node, "end_point", "end_position")
    )


def node_children(node):
    """Return child nodes across Tree-sitter API versions."""
    children = _read_attr(node, "children", "named_children")
    if children is not None:
        return list(children)

    count = _read_attr(node, "child_count", "named_child_count", default=0)
    child_method = getattr(node, "child", None)
    if callable(child_method):
        return [child_method(index) for index in range(int(count))]

    return []


def node_child_by_field_name(node, field_name):
    method = getattr(node, "child_by_field_name", None)
    if callable(method):
        return method(field_name)

    method = getattr(node, "child_by_field", None)
    if callable(method):
        return method(field_name)

    return None


def node_text(node, source_text):
    """Return node text, falling back to slicing the original source."""
    value = _read_attr(node, "text")
    if value is not None:
        return safe_decode(value)

    start_byte = _read_attr(node, "start_byte")
    end_byte = _read_attr(node, "end_byte")
    if start_byte is not None and end_byte is not None:
        source_bytes = source_text.encode("utf-8")
        return source_bytes[int(start_byte):int(end_byte)].decode(
            "utf-8", errors="replace"
        )

    return None


def get_name(node, source_text):
    name_node = node_child_by_field_name(node, "name")
    if name_node is not None:
        return node_text(name_node, source_text)

    for child in node_children(node):
        if node_type(child) in (
            "identifier",
            "type_identifier",
            "property_identifier",
            "constant",
        ):
            return node_text(child, source_text)
    return None


def get_binary_op_text(node, source_text):
    operator_node = node_child_by_field_name(node, "operator")
    if operator_node is not None:
        return node_text(operator_node, source_text)

    for child in node_children(node):
        child_type = node_type(child)
        if child_type in ("or", "and", "||", "&&", "??"):
            return child_type
    return None


def effective_end_row(node):
    end_row, end_col = node_end_point(node)
    start_row, _ = node_start_point(node)
    if end_col == 0 and end_row > start_row:
        end_row -= 1
    return end_row


def analyze_file(content, lang_name):
    parser = get_cached_parser(lang_name)

    # The installed tree_sitter_language_pack version expects str input.
    tree = parser.parse(content)

    root = _read_attr(tree, "root_node")
    if root is None:
        raise AttributeError("Parsed tree does not expose root_node.")

    comment_types = COMMENT_TYPES.get(lang_name, {"comment"})
    class_types = CLASS_TYPES.get(lang_name, set())
    function_types = FUNCTION_TYPES.get(lang_name, set())
    event_map = EVENT_MAP.get(lang_name, {})
    binary_cfg = BINARY_OP_CFG.get(lang_name)
    ternary_node = TERNARY_NODES.get(lang_name)

    comment_rows = set()
    code_rows = set()
    declarations = []
    events = []
    scope_stack = []

    def walk(node):
        current_type = node_type(node)
        start_row, _ = node_start_point(node)
        line_1b = start_row + 1

        if current_type in comment_types:
            end_row = effective_end_row(node)
            for row in range(start_row, end_row + 1):
                comment_rows.add(row)
            return

        pushed = False
        if current_type in class_types:
            name = get_name(node, content)
            kind = CLASS_KIND.get(current_type, "class")
            declarations.append({"type": kind, "name": name, "line": line_1b})
            scope_stack.append(("class", name))
            pushed = True
        elif current_type in function_types:
            name = get_name(node, content)
            is_method = bool(scope_stack) and scope_stack[-1][0] == "class"
            declaration_type = "method" if is_method else "function"
            if name is not None:
                declarations.append(
                    {"type": declaration_type, "name": name, "line": line_1b}
                )
            scope_stack.append(("function", name))
            pushed = True

        current_function = None
        for scope_kind, scope_name in reversed(scope_stack):
            if scope_kind == "function":
                current_function = scope_name
                break

        if current_type in event_map:
            event = {"type": event_map[current_type], "line": line_1b}
            if current_function:
                event["function"] = current_function
            events.append(event)

        if binary_cfg and current_type == binary_cfg[0]:
            operator_text = get_binary_op_text(node, content)
            label = binary_cfg[1].get(operator_text)
            if label:
                event = {"type": label, "line": line_1b}
                if current_function:
                    event["function"] = current_function
                events.append(event)

        if ternary_node and current_type == ternary_node:
            event = {"type": "ternary", "line": line_1b}
            if current_function:
                event["function"] = current_function
            events.append(event)

        children = node_children(node)
        if not children:
            text_value = node_text(node, content)
            if text_value and text_value.strip():
                end_row = effective_end_row(node)
                for row in range(start_row, end_row + 1):
                    code_rows.add(row)
        else:
            for child in children:
                walk(child)

        if pushed:
            scope_stack.pop()

    walk(root)

    declarations.sort(key=lambda declaration: declaration["line"])
    events.sort(key=lambda event: event["line"])
    return comment_rows, code_rows, declarations, events

def build_line_groups(comment_rows, code_rows, start_row, end_row):
    blank = []
    comment_only = []
    inline_comment = []
    code_ranges = []
    current_start = None

    for i in range(start_row, end_row + 1):
        is_code = i in code_rows
        is_comment = i in comment_rows

        if is_code and is_comment:
            inline_comment.append(i + 1)
        elif is_comment:
            comment_only.append(i + 1)
        elif not is_code:
            blank.append(i + 1)

        if is_code:
            if current_start is None:
                current_start = i
        else:
            if current_start is not None:
                code_ranges.append([current_start + 1, i])
                current_start = None

    if current_start is not None:
        code_ranges.append([current_start + 1, end_row + 1])

    groups = []
    if blank:
        groups.append({"type": "blank", "lines": blank})
    if comment_only:
        groups.append({"type": "comment_only", "lines": comment_only})
    if inline_comment:
        groups.append({"type": "inline_comment", "lines": inline_comment})
    if code_ranges:
        groups.append({"type": "code", "ranges": code_ranges})
    return groups


def chunk_file(path, lang_name, content, comment_rows, code_rows,
               declarations, events, chunk_lines):
    total_lines = len(content.splitlines())
    if total_lines == 0:
        return []

    chunks = []
    for chunk_idx, start_row in enumerate(
        range(0, total_lines, chunk_lines), start=1
    ):
        end_row = min(start_row + chunk_lines - 1, total_lines - 1)
        start_1b = start_row + 1
        end_1b = end_row + 1

        line_groups = build_line_groups(comment_rows, code_rows,
                                        start_row, end_row)
        chunk_decls = [d for d in declarations
                       if start_1b <= d["line"] <= end_1b]
        chunk_events = [e for e in events
                        if start_1b <= e["line"] <= end_1b]

        chunks.append({
            "path": path,
            "language": lang_name,
            "chunk": {
                "index": chunk_idx,
                "start_line": start_1b,
                "end_line": end_1b,
            },
            "line_groups": line_groups,
            "declarations": chunk_decls,
            "syntax_events": chunk_events,
        })

    return chunks


def build_fallback_chunks(path, content, chunk_lines):
    text_lines = content.splitlines()
    total = len(text_lines)
    if total == 0:
        return []

    chunks = []
    for chunk_idx, start_row in enumerate(
        range(0, total, chunk_lines), start=1
    ):
        end_row = min(start_row + chunk_lines - 1, total - 1)
        blank = []
        code_ranges = []
        current = None

        for i in range(start_row, end_row + 1):
            if text_lines[i].strip():
                if current is None:
                    current = i
            else:
                blank.append(i + 1)
                if current is not None:
                    code_ranges.append([current + 1, i])
                    current = None

        if current is not None:
            code_ranges.append([current + 1, end_row + 1])

        groups = []
        if blank:
            groups.append({"type": "blank", "lines": blank})
        if code_ranges:
            groups.append({"type": "code", "ranges": code_ranges})

        chunks.append({
            "path": path,
            "language": "unknown",
            "chunk": {
                "index": chunk_idx,
                "start_line": start_row + 1,
                "end_line": end_row + 1,
            },
            "line_groups": groups,
            "declarations": [],
            "syntax_events": [],
        })

    return chunks


def main():
    with open(SOURCE_JSON, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    files = extracted["files"]
    total = len(files)

    print(f"Source     : {SOURCE_JSON}")
    print(f"Total file : {total}")
    print(f"Chunk size : {CHUNK_LINES} baris / chunk")
    print()

    all_chunks = []
    parse_errors = []
    counter = {"ok": 0, "skip": 0, "fallback": 0}
    first_error_printed = False

    for i, file in enumerate(files, start=1):
        path = file["path"]
        ext = file["extension"]
        content = file["content"]
        lang_name = EXT_TO_LANG.get(ext)

        print(f"[{i}/{total}] {path}", end=" ", flush=True)

        if not lang_name or lang_name not in COMMENT_TYPES:
            chunks = build_fallback_chunks(path, content, CHUNK_LINES)
            all_chunks.extend(chunks)
            counter["skip"] += 1
            reason = "ext not mapped" if not lang_name else f"lang '{lang_name}' not configured"
            print(f"SKIP ({reason}) -> {len(chunks)} chunk")
            continue

        try:
            comment_rows, code_rows, decls, events = analyze_file(
                content, lang_name
            )
            chunks = chunk_file(
                path, lang_name, content,
                comment_rows, code_rows, decls, events,
                CHUNK_LINES,
            )
            all_chunks.extend(chunks)
            counter["ok"] += 1
            print(f"OK [{lang_name}] -> {len(chunks)} chunk, "
                  f"{len(decls)} decl, {len(events)} event")
        except Exception as e:
            chunks = build_fallback_chunks(path, content, CHUNK_LINES)
            all_chunks.extend(chunks)
            parse_errors.append((path, lang_name, f"{type(e).__name__}: {e}"))
            counter["fallback"] += 1
            print(f"FALLBACK [{lang_name}] {type(e).__name__}: {e}")
            if not first_error_printed:
                print("    --- full traceback (first error only) ---")
                traceback.print_exc()
                print("    --- end traceback ---")
                first_error_printed = True

    out_dir = Path("data") / extracted["owner"] / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    repo = extracted["repository"]
    out_path = out_dir / f"{repo}.json"

    output = {
        "owner": extracted["owner"],
        "repository": extracted["repository"],
        "default_branch": extracted["default_branch"],
        "chunk_lines": CHUNK_LINES,
        "file_count": total,
        "chunk_count": len(all_chunks),
        "chunks": all_chunks,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"Output     : {out_path.resolve()}")
    print(f"Chunk total: {len(all_chunks)}")
    print()
    print(f"Summary    : {counter['ok']} OK, {counter['skip']} SKIP, "
          f"{counter['fallback']} FALLBACK")
    if counter["ok"] == 0:
        print()
        print("WARNING: NO files were successfully parsed by tree-sitter.")
        print("  All chunks use fallback (just blank vs code, no comment/decl/event).")
        print("  Check: pip show tree-sitter-language-pack")

    if parse_errors:
        print()
        print(f"{len(parse_errors)} file fallback:")
        for path, lang, err in parse_errors[:10]:
            print(f"  [{lang}] {path} : {err}")
        if len(parse_errors) > 10:
            print(f"  ... +{len(parse_errors) - 10} etc.")


if __name__ == "__main__":
    main()

# Run: python -m src.run_ast_analysis