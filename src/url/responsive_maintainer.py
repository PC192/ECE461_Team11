import sys
# import requests
from github import Github, Repository

GITHUB_API_URL = 'https://api.github.com'

def get_weekly_subscore(git_repo: Repository.Repository) -> float:
    response = git_repo.get_stats_code_frequency()

    weekly_additions = 0
    weekly_deletions = 0
    if response is not None:
        for commit_activity in response:
            if commit_activity is not None:
                weekly_additions += commit_activity.additions
                weekly_deletions += commit_activity.deletions
                
    weekly_adds_and_dels = float(weekly_additions - weekly_deletions)
    if weekly_adds_and_dels > 10000000:
        return 1.0
    elif weekly_adds_and_dels > 1000000:
        return 0.75
    elif weekly_adds_and_dels > 100000:
        return 0.5
    elif weekly_adds_and_dels > 10000:
        return 0.25
    else:
        return 0.0


def get_yearly_subscore(git_repo: Repository.Repository) -> float:
    response = git_repo.get_stats_commit_activity()

    yearly_commits = 0
    if response is not None:
        for commit_activity in response:
            if commit_activity is not None:
                yearly_commits += int(commit_activity.total)

    if yearly_commits > 1000:
        return 1.0
    elif yearly_commits > 500:
        return 0.75
    elif yearly_commits > 100:
        return 0.5
    elif yearly_commits > 10:
        return 0.25
    else:
        return 0.0


def get_rm_score(owner: str, repo: str, token: str) -> float:
    # owner, repo = parse_url(url)
    g = Github(token)
    git_repo = g.get_repo(f"{owner}/{repo}")

    # session = requests.Session()
    # session.auth = (token)

    yearly_subscore = get_yearly_subscore(git_repo)
    weekly_subscore = get_weekly_subscore(git_repo)

    rm_score = \
        0.75 * yearly_subscore + \
        0.25 * weekly_subscore

    return rm_score


if __name__ == "__main__":
    # rm_score = 0.64
    rm_score = get_rm_score(sys.argv[1], sys.argv[2], sys.argv[3])
    print(rm_score, end="")