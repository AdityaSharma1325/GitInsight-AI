from pathlib import Path

SUPPORTED = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".go",
    ".md"
}


def get_all_files(repo_path):

    repo_path = Path(repo_path)

    files = []

    for file in repo_path.rglob("*"):

        if file.is_file() and file.suffix in SUPPORTED:

            files.append(file)

    return files