"""Refresh the profile's understated, self-hosted public-project stats card."""

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPOS = [
    "aim-uofa/TVRBench",
    "aim-uofa/MMControl",
    "Li-Liyang/ZJU-OS",
    "Li-Liyang/Game",
    "Li-Liyang/L_Library",
    "Li-Liyang/ZJU-database-DB-minisql",
]


def fetch_repo(repo):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Li-Liyang-project-impact-card",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}", headers=headers
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.load(response)
    return {
        "repo": repo,
        "stars": int(data["stargazers_count"]),
        "forks": int(data["forks_count"]),
    }


def render_card(items, updated_at):
    stars = sum(item["stars"] for item in items)
    forks = sum(item["forks"] for item in items)
    count = len(items)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="224" viewBox="0 0 640 224" role="img" aria-labelledby="title desc">
  <title id="title">Open-source footprint</title>
  <desc id="desc">{stars:,} stars and {forks:,} forks across {count} selected public repositories that Lee owns or contributes to. Updated {updated_at} UTC.</desc>
  <style>
    .panel {{ fill: #F7F5F0; stroke: #E5E0D8; }}
    .heading {{ fill: #504A43; font: 500 17px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
    .note {{ fill: #756D63; font: 400 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
    .value {{ fill: #4B453E; font: 500 34px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-variant-numeric: tabular-nums; }}
    .label {{ fill: #756D63; font: 400 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; letter-spacing: 0.3px; }}
    .rule {{ stroke: #E5E0D8; }}
    .accent {{ fill: #B58D7B; }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: #262522; stroke: #403D37; }}
      .heading, .value {{ fill: #E9E3D9; }}
      .note, .label {{ fill: #B7AEA1; }}
      .rule {{ stroke: #403D37; }}
      .accent {{ fill: #C29C87; }}
    }}
  </style>

  <rect class="panel" x="0.5" y="0.5" width="639" height="223" rx="14"/>
  <circle class="accent" cx="34" cy="36" r="3"/>
  <text class="heading" x="46" y="42">Open-source footprint</text>
  <text class="note" x="32" y="65">Selected public repositories I own or contribute to</text>

  <path class="rule" d="M224 92V153 M424 92V153"/>
  <text class="value" x="32" y="124">{stars:,}</text>
  <text class="label" x="32" y="149">Stars</text>
  <text class="value" x="248" y="124">{forks:,}</text>
  <text class="label" x="248" y="149">Forks</text>
  <text class="value" x="448" y="124">{count}</text>
  <text class="label" x="448" y="149">Repositories</text>

  <path class="rule" d="M32 174H608"/>
  <text class="note" x="32" y="200">A little work, shared.</text>
  <text class="note" x="608" y="200" text-anchor="end">Updated {updated_at} UTC</text>
</svg>
"""


def main():
    # Keep the previous card if any request fails, rather than publishing
    # misleading partial totals.
    items = [fetch_repo(repo) for repo in REPOS]
    updated_at = datetime.now(timezone.utc).strftime("%Y.%m.%d")
    output = Path("assets/project-impact.svg")
    output.parent.mkdir(exist_ok=True)
    output.write_text(render_card(items, updated_at), encoding="utf-8")
    print(f"Updated {output} from {len(items)} public repositories.")


if __name__ == "__main__":
    main()
