import csv
import json
from pathlib import Path

from tree_sitter_language_pack import get_parser


EXTRACTED_PATH = (
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data/"
    "UBCO-COSC499-Winter-2018-Term-1-2/"
    "file_content/"
    "project-1-crm-for-non-profits-trellis-crm.json"
)


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
    ".groovy": "groovy",
    ".graphql": "graphql",
    ".gql": "graphql",
}


LANG_CFG = {
    "python": {
        "comment": {"comment"},
        "function": {"function_definition"},
        "class": {"class_definition"},
        "statement_extras": {"assignment", "augmented_assignment"},
    },
    "javascript": {
        "comment": {"comment"},
        "function": {
            "function_declaration", "function_expression", "arrow_function",
            "method_definition", "generator_function_declaration",
        },
        "class": {"class_declaration"},
        "statement_extras": {"lexical_declaration", "variable_declaration"},
    },
    "typescript": {
        "comment": {"comment"},
        "function": {
            "function_declaration", "function_expression", "arrow_function",
            "method_definition", "method_signature", "function_signature",
        },
        "class": {
            "class_declaration", "interface_declaration",
            "type_alias_declaration", "enum_declaration",
        },
        "statement_extras": {"lexical_declaration", "variable_declaration"},
    },
    "tsx": {
        "comment": {"comment"},
        "function": {
            "function_declaration", "function_expression", "arrow_function",
            "method_definition", "method_signature", "function_signature",
        },
        "class": {
            "class_declaration", "interface_declaration",
            "type_alias_declaration", "enum_declaration",
        },
        "statement_extras": {"lexical_declaration", "variable_declaration"},
    },
    "java": {
        "comment": {"line_comment", "block_comment"},
        "function": {"method_declaration", "constructor_declaration"},
        "class": {
            "class_declaration", "interface_declaration",
            "enum_declaration", "annotation_type_declaration",
        },
        "statement_extras": {"local_variable_declaration", "import_declaration"},
    },
    "go": {
        "comment": {"comment"},
        "function": {"function_declaration", "method_declaration"},
        "class": {"type_declaration"},
        "statement_extras": {
            "short_var_declaration", "var_declaration",
            "const_declaration", "import_declaration",
        },
    },
    "c": {
        "comment": {"comment"},
        "function": {"function_definition"},
        "class": {"struct_specifier", "union_specifier", "enum_specifier"},
        "statement_extras": {"declaration", "preproc_include", "preproc_def"},
    },
    "cpp": {
        "comment": {"comment"},
        "function": {"function_definition"},
        "class": {
            "class_specifier", "struct_specifier",
            "union_specifier", "enum_specifier",
        },
        "statement_extras": {
            "declaration", "preproc_include", "preproc_def",
            "using_declaration",
        },
    },
    "csharp": {
        "comment": {"comment"},
        "function": {
            "method_declaration", "constructor_declaration",
            "destructor_declaration", "local_function_statement",
        },
        "class": {
            "class_declaration", "interface_declaration", "struct_declaration",
            "enum_declaration", "record_declaration",
        },
        "statement_extras": {"local_declaration_statement", "using_directive"},
    },
    "ruby": {
        "comment": {"comment"},
        "function": {"method", "singleton_method"},
        "class": {"class", "module"},
        "statement_extras": {
            "assignment", "operator_assignment", "if", "unless", "while",
            "until", "for", "case", "begin", "return", "break", "next",
            "yield", "redo", "retry",
        },
    },
    "php": {
        "comment": {"comment"},
        "function": {"function_definition", "method_declaration"},
        "class": {
            "class_declaration", "interface_declaration",
            "trait_declaration", "enum_declaration",
        },
        "statement_extras": {
            "use_declaration", "namespace_definition", "namespace_use_declaration",
        },
    },
    "rust": {
        "comment": {"line_comment", "block_comment"},
        "function": {"function_item"},
        "class": {
            "struct_item", "enum_item", "trait_item",
            "impl_item", "union_item",
        },
        "statement_extras": {"let_declaration", "use_declaration"},
    },
    "kotlin": {
        "comment": {"line_comment", "multiline_comment"},
        "function": {"function_declaration"},
        "class": {"class_declaration", "object_declaration"},
        "statement_extras": {"property_declaration", "import_header"},
    },
    "scala": {
        "comment": {"comment", "block_comment"},
        "function": {"function_definition", "function_declaration"},
        "class": {
            "class_definition", "object_definition", "trait_definition",
        },
        "statement_extras": {"val_definition", "var_definition", "import_declaration"},
    },
    "swift": {
        "comment": {"comment", "multiline_comment"},
        "function": {"function_declaration", "init_declaration", "deinit_declaration"},
        "class": {
            "class_declaration", "protocol_declaration",
            "struct_declaration", "enum_declaration",
        },
        "statement_extras": {"property_declaration", "import_declaration"},
    },
    "bash": {
        "comment": {"comment"},
        "function": {"function_definition"},
        "class": set(),
        "statement_extras": {"command", "variable_assignment", "declaration_command"},
    },
    "html": {
        "comment": {"comment"},
        "function": set(),
        "class": set(),
        "statement_extras": set(),
    },
    "css": {
        "comment": {"comment"},
        "function": set(),
        "class": set(),
        "statement_extras": {"rule_set", "at_rule"},
    },
    "scss": {
        "comment": {"comment"},
        "function": {"mixin_statement", "function_statement"},
        "class": set(),
        "statement_extras": {"rule_set", "at_rule", "include_statement"},
    },
    "sql": {
        "comment": {"comment", "marginalia"},
        "function": set(),
        "class": set(),
        "statement_extras": set(),
    },
    "vue": {
        "comment": {"comment"},
        "function": set(),
        "class": set(),
        "statement_extras": set(),
    },
    "svelte": {
        "comment": {"comment"},
        "function": set(),
        "class": set(),
        "statement_extras": set(),
    },
    "groovy": {
        "comment": {"line_comment", "block_comment"},
        "function": {"function_declaration", "method_declaration"},
        "class": {"class_declaration", "interface_declaration"},
        "statement_extras": set(),
    },
    "graphql": {
        "comment": {"comment"},
        "function": set(),
        "class": {"object_type_definition", "interface_type_definition", "enum_type_definition"},
        "statement_extras": set(),
    },
}


_parser_cache = {}


def get_cached_parser(lang_name):
    if lang_name not in _parser_cache:
        _parser_cache[lang_name] = get_parser(lang_name)
    return _parser_cache[lang_name]


def compute_metrics(content, lang_name):
    cfg = LANG_CFG[lang_name]
    parser = get_cached_parser(lang_name)
    tree = parser.parse(content.encode("utf-8"))
    root = tree.root_node

    comment_types = cfg["comment"]
    function_types = cfg["function"]
    class_types = cfg["class"]
    stmt_extras = cfg.get("statement_extras", set())

    comment_rows = set()
    code_rows = set()
    function_count = 0
    class_count = 0
    statement_count = 0

    stack = [root]
    while stack:
        node = stack.pop()
        t = node.type

        if t in comment_types:
            for row in range(node.start_point[0], node.end_point[0] + 1):
                comment_rows.add(row)
            continue

        if t in function_types:
            function_count += 1
        if t in class_types:
            class_count += 1
        if t.endswith("_statement") or t in stmt_extras:
            statement_count += 1

        if node.child_count == 0:
            text = node.text.decode("utf-8", errors="replace")
            if text.strip():
                for row in range(node.start_point[0], node.end_point[0] + 1):
                    code_rows.add(row)
        else:
            stack.extend(node.children)

    text_lines = content.splitlines()
    return {
        "lines": len(text_lines),
        "ncloc": len(code_rows),
        "comment_lines": len(comment_rows - code_rows),
        "statements": statement_count,
        "functions": function_count,
        "classes": class_count,
    }


def fallback_metrics(content):
    text_lines = content.splitlines()
    return {
        "lines": len(text_lines),
        "ncloc": sum(1 for l in text_lines if l.strip()),
        "comment_lines": 0,
        "statements": 0,
        "functions": 0,
        "classes": 0,
    }


def aggregate(rows):
    fields = ["lines", "ncloc", "comment_lines",
              "statements", "functions", "classes"]
    totals = {f: sum(int(r.get(f, 0)) for r in rows) for f in fields}
    totals["files"] = len(rows)
    denom = totals["ncloc"] + totals["comment_lines"]
    totals["comment_density_pct"] = (
        round(totals["comment_lines"] / denom * 100, 2) if denom else 0.0
    )
    return totals


def save_per_file_csv(rows, path):
    fields = ["path", "extension", "language", "lines", "ncloc",
              "comment_lines", "statements", "functions", "classes"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def save_aggregate_csv(totals, meta, path):
    fields = ["owner", "repository", "default_branch", "files", "lines",
              "ncloc", "comment_lines", "comment_density_pct",
              "statements", "functions", "classes"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow({**meta, **totals})


def main():
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    files = extracted["files"]
    total = len(files)

    print(f"Total file : {total}")
    print()

    per_file_rows = []
    parse_errors = []

    for i, file in enumerate(files, start=1):
        path = file["path"]
        ext = file["extension"]
        content = file["content"]
        lang_name = EXT_TO_LANG.get(ext)

        print(f"[{i}/{total}] {path}", end=" ", flush=True)

        if lang_name and lang_name in LANG_CFG:
            try:
                metrics = compute_metrics(content, lang_name)
                row_lang = lang_name
                print(f"OK [{lang_name}]")
            except Exception as e:
                metrics = fallback_metrics(content)
                row_lang = "fallback"
                parse_errors.append((path, str(e)))
                print(f"FALLBACK ({type(e).__name__})")
        else:
            metrics = fallback_metrics(content)
            row_lang = "unknown"
            print("SKIP (no parser)")

        per_file_rows.append({
            "path": path,
            "extension": ext,
            "language": row_lang,
            **metrics,
        })

    metrics_dir = Path("data") / extracted["owner"] / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    repo = extracted["repository"]
    per_file_path = metrics_dir / f"{repo}_per_file.csv"
    aggregate_path = metrics_dir / f"{repo}_aggregate.csv"

    save_per_file_csv(per_file_rows, per_file_path)

    totals = aggregate(per_file_rows)
    meta = {
        "owner": extracted["owner"],
        "repository": extracted["repository"],
        "default_branch": extracted["default_branch"],
    }
    save_aggregate_csv(totals, meta, aggregate_path)

    print()
    print(f"Per-file CSV  : {per_file_path.resolve()} ({len(per_file_rows)} row)")
    print(f"Aggregate CSV : {aggregate_path.resolve()}")
    for k, v in totals.items():
        print(f"  {k:25s} {v}")

    if parse_errors:
        print()
        print(f"{len(parse_errors)} file parse error -> fallback is used:")
        for path, err in parse_errors[:10]:
            print(f"  {path} : {err}")


if __name__ == "__main__":
    main()

# Run: python -m src.run_size_metric_treesitter