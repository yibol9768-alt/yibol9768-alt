"""Refresh the marked README section from public, merged upstream PRs."""

import html
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "yibol9768-alt"
MAX_RECENT_PRS = 8
# Team coursework belongs with personal projects, not upstream contributions.
EXCLUDED_REPOS = ["CollaborativeProjectsX/FusionNN_Yibo"]
START = "<!-- MERGED-PRS:START -->"
END = "<!-- MERGED-PRS:END -->"
QUERY = " ".join([
    "is:pr is:merged is:public",
    f"author:{USERNAME}",
    f"-user:{USERNAME}",
    *(f"-repo:{repo}" for repo in EXCLUDED_REPOS),
    "sort:merged-desc",
])
GRAPHQL = """
query($query: String!, $cursor: String) {
  search(query: $query, type: ISSUE, first: 100, after: $cursor) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number url mergedAt
        repository { nameWithOwner isFork owner { login } }
      }
    }
  }
}
"""


def fetch_prs(token):
    prs, cursor = [], None
    while True:
        request = Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": GRAPHQL, "variables": {
                "query": QUERY, "cursor": cursor,
            }}).encode(),
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json",
                     "User-Agent": "profile-contributions-updater"},
        )
        with urlopen(request, timeout=45) as response:
            result = json.load(response)
        if result.get("errors"):
            raise RuntimeError(f"GitHub query failed: {result['errors']}")
        search = result["data"]["search"]
        if search["issueCount"] > 1000:
            raise RuntimeError("Search limit exceeded; partition queries before updating.")
        for pr in search["nodes"]:
            if not pr or not pr.get("mergedAt"):
                raise RuntimeError("Incomplete PR response; refusing to replace README.")
            repo = pr["repository"]
            if not repo["isFork"] and repo["owner"]["login"].lower() != USERNAME.lower():
                prs.append(pr)
        if not search["pageInfo"]["hasNextPage"]:
            return sorted(prs, key=lambda pr: (pr["mergedAt"], pr["url"]), reverse=True)
        cursor = search["pageInfo"]["endCursor"]


def render(prs):
    repositories = {}
    for pr in sorted(prs, key=lambda pr: (pr["mergedAt"], pr["url"]), reverse=True):
        repo = pr["repository"]["nameWithOwner"]
        repositories.setdefault(repo, []).append(pr)

    lines = [
        f"**{len(prs)} merged PRs · {len(repositories)} upstream repositories**",
        "",
        '<table width="100%">',
        "  <thead>",
        "    <tr>",
        '      <th width="320" align="left" scope="col">Repository</th>',
        '      <th width="110" align="center" scope="col">Merged PRs</th>',
        '      <th width="430" align="left" scope="col">Recent PRs</th>',
        "    </tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for repo, contributions in list(repositories.items())[:10]:
        search_url = "https://github.com/pulls?" + urlencode({
            "q": f"is:pr is:merged author:{USERNAME} repo:{repo}",
        })
        links = " · ".join(
            f'<a href="{html.escape(pr["url"])}">#{pr["number"]}</a>'
            for pr in contributions[:MAX_RECENT_PRS]
        )
        lines.extend([
            "    <tr>",
            f'      <td><strong><a href="https://github.com/{html.escape(repo)}">'
            f'{html.escape(repo)}</a></strong></td>',
            f'      <td align="center"><a href="{html.escape(search_url)}">'
            f'{len(contributions)}</a></td>',
            f"      <td>{links}</td>",
            "    </tr>",
        ])
    if not prs:
        lines.append('    <tr><td>—</td><td align="center">0</td><td>No merged upstream PRs yet.</td></tr>')
    lines.extend(["  </tbody>", "</table>"])
    note = "Updated every 30 minutes."
    if len(repositories) > 10:
        note += " Showing the 10 most recently contributed repositories."
    lines.extend(["", f"<sub>{note}</sub>"])
    return "\n".join(lines)


def update_readme(path, section):
    old = path.read_text()
    if old.count(START) != 1 or old.count(END) != 1:
        raise ValueError("README must have exactly one pair of contribution markers.")
    prefix, rest = old.split(START)
    _, suffix = rest.split(END)
    new = prefix + START + "\n" + section + "\n" + END + suffix
    if new == old:
        return False
    path.write_text(new)
    return True


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN or GITHUB_TOKEN is required.")
    prs = fetch_prs(token)
    changed = update_readme(ROOT / "README.md", render(prs))
    print(f"{'Updated' if changed else 'Unchanged'}: {len(prs)} merged upstream PRs.")
