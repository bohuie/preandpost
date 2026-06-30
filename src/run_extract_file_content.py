import json

from datetime import datetime
from pathlib import Path

from src.extractors.extract_file_content import (extract_files,)


json_path = (
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data/"
    "UBCO-COSC499-Winter-2018-Term-1-2/"
    "project-4-direct-geo-referencing.json"
)


output_root = Path(
    "/Users/aliyahnurdafika/Library/CloudStorage/"
    "OneDrive-UBC/File Hui, Bowen - repo data"
)


with open(json_path, "r", encoding="utf-8",) as file:
    repo_data = json.load(file)

files = extract_files(repo_data)


extracted_at = datetime.now().isoformat()


output = {
    "owner": repo_data["owner"],
    "repository": repo_data["repository"],
    "default_branch": (repo_data["metadata"]["default_branch"]),
    "file_count": len(files),
    "files": files,
    "extracted_at": extracted_at,
}


file_content_path = (
    output_root
    / output["owner"]
    / "file_content"
    / f"{output['repository']}.json"
)

file_content_path.parent.mkdir(parents=True, exist_ok=True,)

with open(file_content_path, "w", encoding="utf-8",) as file:
    json.dump(output, file, indent=2, ensure_ascii=False,)


file_list_output = {
    "owner": output["owner"],
    "repository": output["repository"],
    "default_branch": output["default_branch"],
    "file_count": output["file_count"],

    "paths": [
        item["path"]
        for item in files
    ],

    "filenames": [
        Path(item["path"]).name
        for item in files
    ],

    "extracted_at": extracted_at,
}


file_list_path = (
    output_root
    / output["owner"]
    / "file_list"
    / f"{output['repository']}.json"
)

file_list_path.parent.mkdir(parents=True, exist_ok=True,)

with open(file_list_path, "w", encoding="utf-8",) as file:
    json.dump(file_list_output, file, indent=2, ensure_ascii=False,)


print(f"Repository     : {output['repository']}")
print(f"Default branch : {output['default_branch']}")
print(f"Included files : {output['file_count']}")
print(f"File content   : {file_content_path}")
print(f"File list      : {file_list_path}")


# Run: python -m src.run_extract_file_content