import requests
import json
import os

# GitHub Trending API (for last 7 days)
GITHUB_TRENDING_API = (
    "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"
)

OUTPUT_FILE = "repos.json"


def fetch_trending_repos():
    try:
        response = requests.get(
            GITHUB_TRENDING_API, headers={"Accept": "application/vnd.github.v3+json"}
        )
        if response.status_code == 200:
            data = response.json()["items"][:10]

            repos = [
                {
                    "id": repo["id"],
                    "name": repo["name"],
                    "owner": repo["owner"]["login"],
                    "avatar_url": repo["owner"]["avatar_url"],  # Include avatar
                    "url": repo["html_url"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],  # Ensure forks are included
                    "language": repo["language"],
                    "description": repo["description"],
                }
                for repo in data
            ]

            # Save to JSON file
            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(repos, file, indent=4)

            print(f"✅ Saved {len(repos)} trending repos to {OUTPUT_FILE}")

        else:
            print(f"❌ Error fetching data: {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    fetch_trending_repos()
