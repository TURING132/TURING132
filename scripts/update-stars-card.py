import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

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


items = []
for repo in REPOS:
    try:
        items.append(fetch_repo(repo))
    except Exception as exc:
        print(f"Failed to fetch {repo}: {exc}")

total_stars = sum(item["stars"] for item in items)
total_forks = sum(item["forks"] for item in items)
repo_count = len(items)
updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg width="495" height="210" viewBox="0 0 495 210" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Lee's GitHub Project Stats</title>
  <desc id="desc">Custom GitHub stats card showing total stars, total forks, and repository count across selected public repositories contributed to by Lee.</desc>

  <defs>
    <linearGradient id="headerGradient" x1="0" y1="0" x2="495" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#f6f8fa"/>
      <stop offset="1" stop-color="#ffffff"/>
    </linearGradient>
  </defs>

  <style>
    .card {{
      fill: #ffffff;
      stroke: #d0d7de;
      stroke-width: 1;
    }}
    .header {{
      fill: url(#headerGradient);
    }}
    .title {{
      font: 700 18px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
    .subtitle {{
      font: 400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #57606a;
    }}
    .label {{
      font: 600 13px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
    .value {{
      font: 700 18px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
    .footer {{
      font: 400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #57606a;
    }}
    .divider {{
      stroke: #d8dee4;
      stroke-width: 1;
    }}
    .pill {{
      fill: #f6f8fa;
      stroke: #d0d7de;
      stroke-width: 1;
    }}
    .pill-icon {{
      font: 400 14px -apple-system,BlinkMacSystemFont,"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;
    }}
    .pill-label {{
      font: 600 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #57606a;
    }}
    .pill-value {{
      font: 700 18px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
      fill: #24292f;
    }}
  </style>

  <rect class="card" x="0.5" y="0.5" width="494" height="209" rx="10" />
  <rect class="header" x="1" y="1" width="493" height="64" rx="10" />
  <line class="divider" x1="1" y1="65" x2="494" y2="65" />

  <!-- Logo badge -->
  <circle cx="34" cy="33" r="16" fill="#24292f"/>
  <text x="34" y="38" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="13" font-weight="700" fill="#ffffff">GH</text>

  <text class="title" x="60" y="30">Lee's GitHub Project Stats</text>
  <text class="subtitle" x="60" y="47">Public repositories I own or actively contribute to</text>

  <!-- Card 1 -->
  <rect class="pill" x="20" y="84" width="140" height="78" rx="10" />
  <text class="pill-icon" x="36" y="109">⭐</text>
  <text class="pill-label" x="58" y="109">Total Stars</text>
  <text class="pill-value" x="36" y="139">{total_stars}</text>

  <!-- Card 2 -->
  <rect class="pill" x="177" y="84" width="140" height="78" rx="10" />
  <text class="pill-icon" x="193" y="109">🍴</text>
  <text class="pill-label" x="215" y="109">Total Forks</text>
  <text class="pill-value" x="193" y="139">{total_forks}</text>

  <!-- Card 3 -->
  <rect class="pill" x="334" y="84" width="140" height="78" rx="10" />
  <text class="pill-icon" x="350" y="109">📦</text>
  <text class="pill-label" x="372" y="109">Repositories</text>
  <text class="pill-value" x="350" y="139">{repo_count}</text>

  <text class="footer" x="20" y="187">Updated: {updated_at}</text>
  <text class="footer" x="475" y="187" text-anchor="end">Custom stats for contributed public repos</text>
</svg>
"""

output_dir = Path("assets")
output_dir.mkdir(exist_ok=True)

Path("assets/project-impact.svg").write_text(svg, encoding="utf-8")

print("Generated assets/project-impact.svg")
print(f"Total stars: {total_stars}")
print(f"Total forks: {total_forks}")
print(f"Repositories: {repo_count}")
