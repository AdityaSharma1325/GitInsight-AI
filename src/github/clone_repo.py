from pathlib import Path
from urllib.parse import urlparse

from git import Repo, GitCommandError


# Folder where repositories will be stored
CLONE_DIR = Path("cloned_repos")
CLONE_DIR.mkdir(exist_ok=True)


def validate_github_url(repo_url: str) -> bool:
    """
    Validate whether the given URL is a GitHub repository URL.
    """
    parsed = urlparse(repo_url)

    return (
        parsed.scheme in ("http", "https")
        and parsed.netloc == "github.com"
        and len(parsed.path.strip("/").split("/")) >= 2
    )


def extract_repo_name(repo_url: str) -> str:
    """
    Extract repository name from the URL.

    Example:
    https://github.com/pallets/flask
    -> flask
    """
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    return repo_name


def clone_repository(repo_url: str):
    """
    Clone a GitHub repository if it is not already cloned.

    Returns:
        (success: bool, message: str)
    """

    if not validate_github_url(repo_url):
        return False, "Invalid GitHub repository URL."

    repo_name = extract_repo_name(repo_url)

    destination = CLONE_DIR / repo_name

    if destination.exists():
        return True, destination

    try:
        Repo.clone_from(repo_url, destination)
        return True, destination

    except GitCommandError as e:
        return False, f"Git Error:\n{e}"

    except Exception as e:
        return False, f"An error occurred: {e}"