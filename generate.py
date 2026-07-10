import os
import re
import datetime
import requests

GH_USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ["ACCESS_TOKEN"]
API_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"bearer {TOKEN}"}


def run_query(query, variables=None):
    resp = requests.post(API_URL, json={"query": query, "variables": variables or {}}, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def get_overview():
    query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        followers { totalCount }
        repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
          totalCount
          nodes { stargazerCount }
        }
      }
    }
    """
    data = run_query(query, {"login": GH_USERNAME})["user"]
    stars = sum(r["stargazerCount"] for r in data["repositories"]["nodes"])
    return {
        "created_at": data["createdAt"],
        "followers": data["followers"]["totalCount"],
        "repos": data["repositories"]["totalCount"],
        "stars": stars,
    }


def get_commits_this_year(login):
    year = datetime.datetime.utcnow().year
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
        }
      }
    }
    """
    frm = f"{year}-01-01T00:00:00Z"
    to = f"{year}-12-31T23:59:59Z"
    data = run_query(query, {"login": login, "from": frm, "to": to})["user"]
    return data["contributionsCollection"]["totalCommitContributions"]


def member_since(created_at):
    dt = datetime.datetime.strptime(created_at[:10], "%Y-%m-%d")
    return dt.strftime("%B %Y")


def set_tspan_value(content, element_id, value):
    pattern = re.compile(r'(<tspan id="' + element_id + r'">)(.*?)(</tspan>)')
    return pattern.sub(lambda m: m.group(1) + str(value) + m.group(3), content)


def update_svg(path, values):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for element_id, value in values.items():
        content = set_tspan_value(content, element_id, value)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    overview = get_overview()
    commits = get_commits_this_year(GH_USERNAME)
    values = {
        "REPOS": overview["repos"],
        "STARS": overview["stars"],
        "FOLLOWERS": overview["followers"],
        "COMMITS": commits,
        "MEMBER_SINCE": member_since(overview["created_at"]),
        "LAST_UPDATED": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
    }
    for svg_file in ("dark_mode.svg", "light_mode.svg"):
        update_svg(svg_file, values)


if __name__ == "__main__":
    main()
