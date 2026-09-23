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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="480" height="136" viewBox="0 0 480 136" role="img" aria-labelledby="title desc">
  <title id="title">Open source</title>
  <desc id="desc">{stars:,} stars and {forks:,} forks across {count} selected public repositories that Lee owns or contributes to. Updated {updated_at} UTC.</desc>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }}
    .heading {{ fill: #48443F; font-size: 15px; font-weight: 500; }}
    .summary {{ fill: #626262; font-size: 24px; font-weight: 400; letter-spacing: -0.4px; }}
    .value {{ fill: #A17D6B; font-weight: 500; font-variant-numeric: tabular-nums; }}
    .separator {{ fill: #C9C3BB; }}
    .note {{ fill: #717171; font-size: 12px; }}
    .rule {{ stroke: #E9E9E9; }}
    .accent {{ stroke: #B58D7B; }}
    @media (prefers-color-scheme: dark) {{
      .heading {{ fill: #EEE8DE; }}
      .summary {{ fill: #C7C1B8; }}
      .value {{ fill: #C5A08B; }}
      .separator {{ fill: #625C54; }}
      .note {{ fill: #A39C93; }}
      .rule {{ stroke: #383631; }}
      .accent {{ stroke: #B58D7B; }}
    }}
  </style>

  <!-- Transparent, unboxed layout: a small editorial section, not a dashboard. -->
  <text class="heading" x="0" y="24">Open source</text>
  <path class="rule" d="M0 40H480"/>
  <path class="accent" d="M0 40H32" stroke-width="2"/>
  <text class="summary" x="0" y="83"><tspan class="value">{stars:,}</tspan> stars<tspan class="separator"> · </tspan><tspan class="value">{forks:,}</tspan> forks<tspan class="separator"> · </tspan><tspan class="value">{count}</tspan> projects</text>
  <text class="note" x="0" y="114">Selected public repositories I own or contribute to.</text>
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
