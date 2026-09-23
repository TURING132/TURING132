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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="480" height="32" viewBox="0 0 480 32" role="img" aria-labelledby="title desc">
  <title id="title">Open source</title>
  <desc id="desc">{stars:,} stars and {forks:,} forks across {count} selected public repositories that Liyang Li owns or contributes to. Updated {updated_at} UTC.</desc>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }}
    .summary {{ fill: #626262; font-size: 16px; font-weight: 400; }}
    .value {{ fill: #A17D6B; font-weight: 500; font-variant-numeric: tabular-nums; }}
    .separator {{ fill: #C9C3BB; }}
    @media (prefers-color-scheme: dark) {{
      .summary {{ fill: #C7C1B8; }}
      .value {{ fill: #C5A08B; }}
      .separator {{ fill: #625C54; }}
    }}
  </style>

  <!-- A transparent inline summary, with no visible container or decoration. -->
  <text class="summary" x="0" y="21"><tspan class="value">{stars:,}</tspan> stars<tspan class="separator"> · </tspan><tspan class="value">{forks:,}</tspan> forks<tspan class="separator"> · </tspan><tspan class="value">{count}</tspan> selected projects</text>
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
