import os

from dotenv import load_dotenv

from src.extractors.github_client import GithubClient

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("Please add GITHUB_TOKEN to the .env file.")

client = GithubClient(token=token)

data = client.fetch_full(
    owner="UBCO-COSC499-Winter-2018-Term-1-2",
    repo="project-8-ar-vr-experience-team-8-ar-vr",
)

output_path = client.save_repository_json(data)

print("Saved to:", output_path)
print("Manifest:", data["manifest"])

# Run: python -m src.run_github_client