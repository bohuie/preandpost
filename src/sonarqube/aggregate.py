import os
import csv

BASE_DIR = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/SonarQube"
INPUT_DIR = os.path.join(BASE_DIR, "repos")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "aggregated.csv")
INPUT_CSV = "sonar_repos.csv"

FOLDERS = {"UBCO-COSC499-SUMMER-2018": ("pre", 2018), "UBCO-COSC499-Winter-2018-Term-1-2": ("pre", 2018),
    "ubco-cosc499-summer2019": ("pre", 2019), "UBCO-COSC499-Summer-2020": ("pre", 2020), 
    "UBCO-COSC-499-Summer-2022": ("pre", 2022), "COSC-499-W2023": ("post", 2023),
    "UBCO-COSC-499-Summer-2023": ("post", 2023), "COSC-499-W2024": ("post", 2024),
    "COSC-499-W2025": ("post", 2025), "UBCO-COSC499-S2025": ("post", 2025),
}

AVG_PER_REPO = [
    "vulnerabilities", "bugs", "code_smells", "sqale_index", "duplicated_lines", "duplicated_blocks", "duplicated_files",
    "ncloc", "lines", "statements", "functions", "classes", "files", "comment_lines", "complexity", "cognitive_complexity",
]

RATIO_METRICS = [
    "sqale_debt_ratio", "duplicated_lines_density", "comment_lines_density",
]

RATING_METRICS = [
    "security_rating", "reliability_rating", "sqale_rating",
]

GRADES = ["A", "B", "C", "D", "E"]
RATING_MAP = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}

def to_float(value):
    # Convert a value to float, return None if conversion fails
    try:
        return float(str(value).strip())
    except ValueError:
        return None

def to_grade(value):
    # In CSV files, ratings are stored as numbers (1-5). Convert to grades (A-E) for easier understanding
    number = to_float(value)

    if number is None:
        return None

    return RATING_MAP.get(int(round(number)))

def find_csv_files(folder_path):
    csv_files = []

    if not os.path.exists(folder_path):
        return csv_files

    for root, _, files in os.walk(folder_path): # Go to the main folder and all subfolders within it
        if INPUT_CSV in files:  # Check if the target CSV file exists in the current folder
            csv_path = os.path.join(root, INPUT_CSV) # If yes, create a full path to the file
            csv_files.append(csv_path)  # Enter the file path into the list

    return csv_files

def read_rows(csv_files):
    all_csv_rows = []

    for csv_file in csv_files:
        with open(csv_file, encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))   # Read the contents of a csv and convert it to a list of dictionaries

        all_csv_rows.append((csv_file, rows)) 

    return all_csv_rows

def add_metrics(row, metrics, totals, counts):
    ''' Sum metric values into totals and track how many valid values were seen (used for averaging by valid-count later). '''
    for metric in metrics:
        value = to_float(row.get(metric))

        if value is not None:
            totals[metric] += value # Sum the value of the metric into the total for that metric
            counts[metric] += 1     # Count how many valid values were seen for that metric 

def add_rating_metrics(row, ratings):
    ''' Rating metrics are converted to grades and counted. '''
    for metric in RATING_METRICS:
        grade = to_grade(row.get(metric))

        if grade is not None:
            ratings[metric][grade] += 1 

def build_result(period, year, folder, team_count, csv_count, rows_count, totals, avg_counts, ratio_totals, ratio_counts, ratings):
    result = {
        "period": period,
        "year": year,
        "organization_folder": folder,
        "team_count": team_count,
        "csv_files_found": csv_count,
        "rows_count": rows_count,
    }

    for metric in AVG_PER_REPO:
        result[metric] = round(totals[metric] / avg_counts[metric], 4) if avg_counts[metric] else 0

    for metric in RATIO_METRICS:
        result[metric] = round(ratio_totals[metric] / ratio_counts[metric], 4) if ratio_counts[metric] else 0

    for metric in RATING_METRICS:
        for grade in GRADES:
            result[f"{metric}_{grade}"] = ratings[metric][grade]

    return result

def aggregate_folder(folder, period, year):
    folder_path = os.path.join(INPUT_DIR, folder)

    if not os.path.exists(folder_path):
        print(f"WARNING: Folder not found, skipping: {folder_path}")
        return None

    csv_files = find_csv_files(folder_path)

    totals = {metric: 0.0 for metric in AVG_PER_REPO}
    avg_counts = {metric: 0 for metric in AVG_PER_REPO}
    ratio_totals = {metric: 0.0 for metric in RATIO_METRICS}
    ratio_counts = {metric: 0 for metric in RATIO_METRICS}
    ratings = {
        metric: {grade: 0 for grade in GRADES}
        for metric in RATING_METRICS
    }

    team_count = 0
    rows_count = 0

    for csv_file, rows in read_rows(csv_files):
        if not rows:
            print(f"WARNING: Empty CSV, skipping: {csv_file}")
            continue

        team_count += 1
        rows_count += len(rows)

        for row in rows:
            add_metrics(row, AVG_PER_REPO, totals, avg_counts)
            add_metrics(row, RATIO_METRICS, ratio_totals, ratio_counts)
            add_rating_metrics(row, ratings)

    print(f"{year} | {period.upper()} | {folder}: {len(csv_files)} CSV, {team_count} teams")

    return build_result(
        period, year, folder, team_count, len(csv_files), rows_count,
        totals, avg_counts, ratio_totals, ratio_counts, ratings
    )

def write_output(rows):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {OUTPUT_CSV}")

def main():
    rows = [
        aggregate_folder(folder, period, year)  # Run aggregate_folder() for each folder in FOLDERS
        for folder, (period, year) in FOLDERS.items()
    ]

    rows = [row for row in rows if row is not None] # Skip empty rows (folders that were not found or had no CSV files)
    rows.sort(key=lambda row: (row["year"], row["organization_folder"])) # To sort results by year and organization_folder

    write_output(rows)

    print("\nDone.")

if __name__ == "__main__":
    main()

# Run:
# python -m src.sonarqube.aggregate