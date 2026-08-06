from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".php",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css"
}

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules"
}

def load_repository_files(repo_path):
    """
    Reads all supported files from the repository.
    """

    repo_path = Path(repo_path)

    documents = []

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if any(folder in IGNORE_DIRS for folder in file.parts):
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            documents.append(
                {
                    "source": str(file.relative_to(repo_path)),
                    "content": content,
                    "extension": file.suffix.lower()
                }
            )

        except Exception:
            pass

    
    return documents
