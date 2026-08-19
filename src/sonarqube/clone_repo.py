import subprocess
import os

def clone_repo(repo_url, organization_name, repo_name):
    """
    Clones a git repository into the specified directory structure.
    Target: /Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/clone_repo/{organization_name}/{repo_name}
    """
    # Place of clone results
    base_path = "/Users/aliyahnurdafika/Library/CloudStorage/OneDrive-UBC/File Hui, Bowen - repo data/clone_repo"
    
    # Inside the clone_repo folder, create subfolders for organization_name and repo_name
    target_dir = os.path.join(base_path, organization_name, repo_name)
    
    # Create a directory if it does not exist
    if not os.path.exists(target_dir):
        print(f"Creating directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)
    else:
        print(f"Directory already exists: {target_dir}")
        subprocess.run(["git", "pull"], cwd=target_dir, check=True)  # Update repo if it already exists
        return target_dir

    print(f"Cloning {repo_url} into {target_dir}...")

    # python -m => main process, git clone => sub process
    
    try:
        # Running the git clone command on target_dir
        subprocess.run(["git", "clone", repo_url, "."], cwd=target_dir, check=True)
        print("Cloning successful!")
        return target_dir
    except subprocess.CalledProcessError as e:
        print(f"Error during cloning: {e}")
        return None

if __name__ == "__main__":
    ORG = "COSC-499-W2023"
    REPO_NAME = "year-long-project-team-22"
    URL = "https://github.com/COSC-499-W2023/year-long-project-team-22.git" 
    
    clone_repo(URL, ORG, REPO_NAME)

# Run: python3 -m src.sonarqube.clone_repo 