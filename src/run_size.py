"""
Runs Size metric extraction for one cloned repository at a time.

Input folder structure:
data/
└── repos/
    └── <REPO_OWNER>/
        └── <REPO_NAME>/

Example input:
data/
└── repos/
    └── COSC-499-W2023/
        └── year-long-project-team-15/

Output folder structure:
data/
└── outputs/
    └── size/
        └── <REPO_OWNER>/
            └── <REPO_NAME>.csv    # File-level metrics for one repository

Example output:
data/
└── outputs/
    └── size/
        └── COSC-499-W2023/
            └── year-long-project-team-15.csv
"""

import os
import csv  # To create CSV file
from metrics.size import analyze_repository

# Only runs when executed directly, not when imported by another script
if __name__ == "__main__":
    REPO_OWNER = "COSC-499-W2023"
    REPO_NAME = "year-long-project-team-15"

    input_path = "./data/repos/" + REPO_OWNER + "/" + REPO_NAME
    if not os.path.exists(input_path):
        print(f"Repository folder not found: {input_path}. Please check REPO_OWNER, REPO_NAME, or clone the repository first")
    else:
        repository_metrics, file_metrics = analyze_repository(input_path)
        output_path = "./data/outputs/size/" + REPO_OWNER       # Save CSV output in this path
        # But we need to make sure that this folder path already exist before we create CSV file
        os.makedirs(output_path, exist_ok=True)  # Create a folder if it doesn't exist. If the folder already exists, just continue
        output_csv = output_path + "/" + REPO_NAME + ".csv"

        fieldnames = [
            "repo_owner",
            "repo_name",
            "file_path",
            "language",
            "lines",
            "sloc",
            "comment_lines",
            "comment_density",
            "statements",
            "functions",
            "classes",
        ]

        with open(output_csv, mode="w", newline="", encoding = "utf-8") as csv_file: # Open CSV in write mode
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
            
            writer.writeheader()    # Write the first CSV row based on fieldnames

            for metric in file_metrics:
                row = {                             # One row represents one file
                    "repo_owner": REPO_OWNER,
                    "repo_name": REPO_NAME,
                    "file_path": metric.file_path,
                    "language": metric.language,
                    "lines": metric.lines,
                    "sloc": metric.sloc,
                    "comment_lines": metric.comment_lines,
                    "comment_density": metric.comment_density,
                    "statements": metric.statements,
                    "functions": metric.functions,
                    "classes": metric.classes,
                }
                writer.writerow(row)    # Write one row to the CSV
        
        print(f"Successfully analyzed: {REPO_OWNER}/{REPO_NAME}")
        print(f"Total files analyzed: {len(file_metrics)}")
        print(f"CSV output: {output_csv}")
