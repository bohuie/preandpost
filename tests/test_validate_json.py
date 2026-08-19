""" Unit test:

1. Arrange: Prepare data or initial conditions. 
2. Act: Run the function or method to be tested. 
3. Assert: To ensure the output meets expectations. To test whether a condition in our code returns True.
Otherwise, the program will throw an AssertionError


"""
import json

def test_2018_project_1_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-1-crm-for-non-profits-trellis-crm.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 89        # Count how many PRs are stored in json


def test_2018_project_3_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-3-analog-gauge-reader-cs_visionaries.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 48


def test_2018_project_4_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-4-direct-geo-referencing.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 154


def test_2018_project_8_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-8-ar-vr-experience-team-8-ar-vr.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 3


def test_2018_project_9_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-9-radio-telescope-web-public-interface-project-space-odyssey.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 3


def test_2018_project_11_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-11-indoor-wayfinding-indoor-wayfinding.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 65


def test_2018_project_12_total_PR():
    file_path = "data/UBCO-COSC499-Winter-2018-Term-1-2/project-12-bus-advisory-offline-real-time-bus-location-tracker.json"

    # Parse JSON file into Python dictionary, since it was originally still text/string
    with open(file_path, "r", encoding="utf-8") as file:
        repo_data = json.load(file)

    assert "pull_requests" in repo_data
    assert len(repo_data["pull_requests"]) == 49

# Run: python -m pytest src/test_validate_json.py