from pathlib import Path

from src.llm.client import get_llm_client

MODEL_NAME = "llama-3.3-70b-versatile"


def detect_dependencies(repo_path):
    """
    Analyze repository technologies.
    """

    repo_path = Path(repo_path)

    context = []

    important_files = [
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "Dockerfile",
        "README.md"
    ]

    for filename in important_files:

        file = repo_path / filename

        if file.exists():

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                context.append(
                    f"{filename}\n\n{content}"
                )

            except Exception:
                pass

    prompt = f"""
You are a Senior Software Architect.

Analyze the repository.

Identify:

1. Programming Languages
2. Frameworks
3. Libraries
4. AI Models
5. Embedding Models
6. Vector Database
7. Build Tools
8. Deployment
9. Missing Technologies

Repository Files:

{chr(10).join(context)}
"""

    client = get_llm_client()

    response = client.chat.completions.create(

        model=MODEL_NAME,

        temperature=0.2,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response.choices[0].message.content