import requests
import os
import json
import csv
from dotenv import load_dotenv

load_dotenv(override=True)

def fetch_and_save_metrics(project_key, organization, repo_name):
    """
    Fetch repository level metrics data and save to JSON & CSV.
    """
    sonar_url = os.getenv("SONAR_HOST_URL", "http://localhost:9000")
    token = os.getenv("SONAR_TOKEN")
    
    if not token:
        print("Error: SONAR_TOKEN not found in .env file!")
        return

    # Path target
    base_path = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/SonarQube/repos"
    target_dir = os.path.join(base_path, organization, repo_name)   # repo_name 
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    json_path = os.path.join(target_dir, "sonar_repos.json")
    csv_path = os.path.join(target_dir, "sonar_repos.csv")
    
    metrics = (
        "vulnerabilities,security_rating,bugs,reliability_rating,sqale_rating,"
        "code_smells,sqale_index,sqale_debt_ratio,complexity,cognitive_complexity,"
        "duplicated_lines_density,duplicated_lines,duplicated_blocks,duplicated_files,"
        "ncloc,lines,statements,functions,classes,files,comment_lines,"
        "comment_lines_density,blocker_violations,critical_violations,major_violations,"
        "minor_violations,line_coverage,lines_to_cover,uncovered_lines"
    )
    
    # curl -u <token>: "http://localhost:9000/api/measures/component?component=<project_key>&metricKeys=<metrics>"
    endpoint = f"{sonar_url}/api/measures/component"
    params = {"component": project_key, "metricKeys": metrics}
    
    print(f"Fetching metrics for: {project_key}...")
    response = requests.get(endpoint, params=params, auth=(token, ''))
    
    if response.status_code >= 200 and response.status_code < 300:
        data = response.json()
        
        # 1. Save JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)    # Save json to sonar_repos.json
        
        # 2. Process to CSV
        component = data.get("component", {})
        measures = component.get("measures", [])
        
        # Create a dictionary for CSV rows (repo name + all metrics)
        row = {"project_name": component.get("name")}
        for m in measures:
            row[m["metric"]] = m.get("value", "0")
            
        # Write to CSV
        header = ["project_name"] + [m["metric"] for m in measures]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerow(row)
            
        print(f"Success! Saved JSON: {json_path}")
        print(f"Success! Saved CSV: {csv_path}")
    else:
        print(f"Error! Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_and_save_metrics(
        project_key="W2023-team-21", 
        organization="COSC-499-W2023",
        repo_name="year-long-project-team-21"
    )

# Run: python3 -m src.sonarqube.run_sonar_repos