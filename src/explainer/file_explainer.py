from pathlib import Path

from src.llm.client import get_llm_client

MODEL_NAME = "llama-3.3-70b-versatile"


def explain_file(file_path: str):

    file = Path(file_path)

    code = file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    prompt = f"""
You are a Senior Software Engineer.

Explain this file.

Include:

1. Purpose

2. Main Functions

3. Workflow

4. Inputs

5. Outputs

6. Dependencies

7. Improvements

Code:

{code}
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