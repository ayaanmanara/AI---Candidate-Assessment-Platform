import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GRAPHQL_URL = "https://api.github.com/graphql"

# This query pulls profile stats, contribution calendar, and repos with commit history
QUERY = """
query($username: String!) {
  user(login: $username) {
    name
    login
    avatarUrl
    bio
    followers { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
    repositories(first: 5, orderBy: {field: PUSHED_AT, direction: DESC}, isFork: false, privacy: PUBLIC) {
      nodes {
        name
        description
        url
        stargazerCount
        forkCount
        primaryLanguage {
          name
        }
        languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
            }
          }
        }
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 20) {
                totalCount
                nodes {
                  message
                  committedDate
                  additions
                  deletions
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

def test_fetch(username: str):
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    response = httpx.post(
        GRAPHQL_URL,
        json={"query": QUERY, "variables": {"username": username}},
        headers=headers,
        timeout=15.0
    )

    if response.status_code != 200:
        print(f"Failed with status code {response.status_code}: {response.text}")
        return

    data = response.json()
    if "errors" in data:
        print(f"GraphQL returned errors: {data['errors']}")
        return

    user_data = data["data"]["user"]
    print("\n--- Success! Data Summary ---")
    print(f"User: {user_data.get('name')} (@{user_data.get('login')})")
    print(f"Total Calendar Contributions: {user_data['contributionsCollection']['contributionCalendar']['totalContributions']}")
    print(f"Fetched Repositories Count: {len(user_data['repositories']['nodes'])}")
    
    for repo in user_data['repositories']['nodes']:
        print(f"\n- Repo: {repo['name']} (Language: {repo.get('primaryLanguage', {}).get('name') if repo.get('primaryLanguage') else 'None'})")
        branch = repo.get('defaultBranchRef')
        if branch and branch.get('target'):
            commit_count = branch['target']['history']['totalCount']
            recent_commits = len(branch['target']['history']['nodes'])
            print(f"  Total Commits: {commit_count} (Fetched latest {recent_commits} commits)")

if __name__ == "__main__":
    # Test with your own username or any active public GitHub profile
    target_user = input("Enter a GitHub username to test: ").strip()
    test_fetch(target_user)
