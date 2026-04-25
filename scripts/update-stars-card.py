import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from html import escape

REPOS = [
    "aim-uofa/MMControl",
    "TURING132/ZJU-OS",
    "TURING132/L_Library",
    "TURING132/ZJU-database-DB-minisql",
    "TURING132/Game"
]

TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "TURING132-project-impact-card",
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


def shorten(text, max_len=28):
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


items = []
for repo in REPOS:
    try:
        items.append(fetch_repo(repo))
    except Exception as exc:
        print(f"Failed to fetch {repo}: {exc}")

items.sort(key=lambda x: x["stars"], reverse=True)

total_stars = sum(item["stars"] for item in items)
total_forks = sum(item["forks"] for item in items)
repo_count = len(items)

if items:
    top_repo = items[0]["repo"]
    top_repo_stars = items[0]["stars"]
else:
    top_repo = "N/A"
    top_repo_stars = 0

top_repo_display = f"{shorten(top_repo)} ({top_repo_stars}★)"
updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Lee's GitHub Project Stats</title>
  <desc id="desc">Custom GitHub stats card showing total stars, forks, contributed repositories, and top repository across selected public repositories.</desc>

  <style>
    .bg {{
      fill: #ffffff;
      stroke: #e4e2e2;
      stroke-width: 1;
      rx: 8;
    }}
    .title {{
      font: 600 18px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #0366d6;
    }}
    .subtitle {{
      font: 400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #586069;
    }}
    .label {{
      font: 600 13px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
    .value {{
      font: 600 13px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
    .icon {{
      font: 400 14px -apple-system,BlinkMacSystemFont,"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;
    }}
    .line {{
      stroke: #eaecef;
      stroke-width: 1;
    }}
    .footer {{
      font: 400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #586069;
    }}
  </style>

  <rect class="bg" x="0.5" y="0.5" width="494" height="194" rx="8" />

  <text class="title" x="25" y="35">Lee's GitHub Project Stats</text>
  <text class="subtitle" x="25" y="54">Public repositories I own or actively contribute to</text>

  <line class="line" x1="25" y1="68" x2="470" y2="68" />

  <text class="icon" x="28" y="92">⭐</text>
  <text class="label" x="50" y="92">Total Stars Earned:</text>
  <text class="value" x="468" y="92" text-anchor="end">{total_stars}</text>

  <text class="icon" x="28" y="118">🍴</text>
  <text class="label" x="50" y="118">Total Forks:</text>
  <text class="value" x="468" y="118" text-anchor="end">{total_forks}</text>

  <text class="icon" x="28" y="144">📦</text>
  <text class="label" x="50" y="144">Contributed Repositories:</text>
  <text class="value" x="468" y="144" text-anchor="end">{repo_count}</text>

  <text class="icon" x="28" y="170">🏆</text>
  <text class="label" x="50" y="170">Top Repository:</text>
  <text class="value" x="468" y="170" text-anchor="end">{escape(top_repo_display)}</text>

  <text class="footer" x="25" y="187">Updated: {updated_at}</text>
</svg>
"""

output_dir = Path("assets")
output_dir.mkdir(exist_ok=True)

Path("assets/project-impact.svg").write_text(svg, encoding="utf-8")

print("Generated assets/project-impact.svg")
print(f"Total stars: {total_stars}")
print(f"Total forks: {total_forks}")
print(f"Top repo: {top_repo_display}")
