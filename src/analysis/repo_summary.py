from pathlib import Path
from collections import Counter

# ignore unnecessary folders
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}

# Map extensions to readable language names
EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".txt": "Text",
    ".csv": "CSV",
    ".ipynb": "Jupyter Notebook",
    ".toml": "TOML",
    ".xml": "XML",
}

def get_repository_files(repo_path: str):
    """
    Returns all valid files inside the repository.
    """

    repo_path = Path(repo_path)

    files = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if any(folder in IGNORE_DIRS for folder in file.parts):
            continue

        files.append(file)

    return files


def count_languages(files):
    """
    Count files by programming language.
    """

    counter = Counter()

    for file in files:

        language = EXTENSION_MAP.get(
            file.suffix.lower(),
            "Other"
        )

        counter[language] += 1

    return dict(counter)


def get_largest_files(files, top_n=5):
    """
    Return largest files in repository.
    """

    largest = sorted(
        files,
        key=lambda file: file.stat().st_size,
        reverse=True
    )[:top_n]

    result = []

    for file in largest:

        result.append(
            {
                "name": file.name,
                "size_kb": round(file.stat().st_size / 1024, 2)
            }
        )

    return result


def get_repository_size(files):
    """
    Return total repository size in kilobytes.
    """

    total_bytes = sum(file.stat().st_size for file in files)

    return round(total_bytes / 1024, 2)


def analyze_repository(repo_path: str):
    repo_path = Path(repo_path)

    print("=" * 50)
    print("Repository Path:", repo_path)
    print("Exists:", repo_path.exists())
    print("Is Directory:", repo_path.is_dir())

    files = get_repository_files(repo_path)

    print("Files Found:", len(files))
    for file in files[:10]:
        print(file)

    print("=" * 50)

    return {
        "repository_name": repo_path.name,
        "total_files": len(files),
        "languages": count_languages(files),
        "largest_files": get_largest_files(files),
        "repository_size_kb": get_repository_size(files)
    }