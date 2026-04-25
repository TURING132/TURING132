import os
import json
import urllib.request
from pathlib import Path

REPOS = [
    "aim-uofa/MMControl",
    "aim-uofa/aim-uofa.github.io",
    "TURING132/ActiveSpatial",
    "TURING132/ActiveSpatial-Nips",
    "TURING132/ZJU-OS",
    "TURING132/L_Library",
    "TURING132/ZJU-database-DB-minisql",
]

TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "TURING132-profile-stars-card",
}

if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"


def fetch_repo(repo):
    url = f"https://api.github.com/repos/{repo}"
    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    return {
        "repo": repo,
        "stars": int(data.get("stargazers_count", 0)),
        "forks": int(data.get("forks_count", 0)),
    }


items = []
for repo in REPOS:
    try:
        items.append(fetch_repo(repo))
    except Exception as exc:
        print(f"Failed to fetch {repo}: {exc}")

total_stars = sum(item["stars"] for item in items)
total_forks = sum(item["forks"] for item in items)
repo_count = len(items)

svg = f"""<svg width="495" height="150" viewBox="0 0 495 150" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Public Project Impact</title>
  <desc id="desc">Total stars and forks across selected public repositories contributed to by Lee.</desc>

  <style>
    .card {{
      fill: #ffffff;
      stroke: #e4e2e2;
      stroke-width: 1;
    }}
    .title {{
      font: 600 18px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      fill: #2f80ed;
    }}
    .label {{
      font: 500 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      fill: #586069;
    }}
    .value {{
      font: 700 24px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      fill: #24292e;
    }}
    .small {{
      font: 400 12px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      fill: #586069;
    }}
  </style>

  <rect class="card" x="0.5" y="0.5" width="494" height="149" rx="8" />

  <text class="title" x="24" y="36">Public Project Impact</text>

  <text class="label" x="24" y="70">⭐ Stars from contributed repos</text>
  <text class="value" x="24" y="105">{total_stars}</text>

  <text class="label" x="210" y="70">🍴 Forks</text>
  <text class="value" x="210" y="105">{total_forks}</text>

  <text class="label" x="340" y="70">📦 Repositories</text>
  <text class="value" x="340" y="105">{repo_count}</text>

  <text class="small" x="24" y="132">Includes selected public repositories owned by or contributed to by TURING132.</text>
</svg>
"""

output_dir = Path("assets")
output_dir.mkdir(exist_ok=True)
Path("assets/project-impact.svg").write_text(svg, encoding="utf-8")

print(f"Generated assets/project-impact.svg")
print(f"Total stars: {total_stars}")
print(f"Total forks: {total_forks}")
