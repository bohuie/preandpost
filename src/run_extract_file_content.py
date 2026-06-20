import json
from src.extractors.extract_file_content import extract_files
from datetime import datetime
from pathlib import Path

json_path = ("/Users/aliyahnurdafika/Documents/preandpost/data/UBCO-COSC499-Winter-2018-Term-1-2/project-1-crm-for-non-profits-trellis-crm.json")

with open(json_path, "r", encoding="utf-8") as f:
    repo_data = json.load(f)

    files = extract_files(repo_data)

    output = {
        "owner": repo_data["owner"],
        "repository": repo_data["repository"],
        "default_branch": repo_data["metadata"]["default_branch"],
        "file_count": len(files),
        "files": files,
        "extracted_at": datetime.now().isoformat()
    }

    output_path = (Path("data")/output["owner"]/"file_content"/f"{output['repository']}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent = 2)

    file_list_output = {
        "owner": output["owner"],
        "repository": output["repository"],
        "default_branch": output["default_branch"],
        "file_count": output["file_count"],
        "paths": [item["path"] for item in files],
        "extracted_at": output["extracted_at"],
    }

    file_list_path = (Path("data")/output["owner"]/"file_list"/f"{output['repository']}.json")
    file_list_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_list_path, "w", encoding="utf-8") as f:
        json.dump(file_list_output, f, indent=2)

# Run: python -m src.run_extract_file_content

# Run: python -m src.run_extract_file_content