import httpx
from google import genai
from config import GEMINI_API_KEY
import json


client = genai.Client(api_key=GEMINI_API_KEY)

async def ai_review_diff(diff_text: str,repo_name:str, pr_number:int) -> str:

    prompt = f"""
        You are a senior software engineer performing a pull request review.

        Repository: {repo_name}
        PR Number: {pr_number}

        Your job is to review ONLY the code changes introduced in this diff.

        IMPORTANT RULES:

        1. ONLY review added ("+") lines and the behavior introduced by those changes.
        2. DO NOT comment on pre-existing code.
        3. DO NOT suggest general refactoring.
        4. DO NOT suggest architectural improvements.
        5. DO NOT suggest replacing libraries, frameworks, or UI components unless the change itself introduces a problem.
        6. DO NOT make style-only comments.
        7. DO NOT comment on naming preferences.
        8. DO NOT comment on code that was not modified.
        9. If a changed line is acceptable, do not create an issue for it.
        10. Ignore purely subjective preferences.
        11. Maximum 5 issues.

        Report issues only when the change introduces:

        - Security vulnerabilities
        - Functional bugs
        - Logic errors
        - Data corruption risks
        - Reliability problems
        - Significant performance regressions
        - Broken validation
        - Incorrect API usage

        Severity definitions:

        - critical = security issue, crash, data loss, or broken functionality
        - warning = bug risk or reliability concern
        - suggestion = meaningful improvement directly related to the change

        Line Number Rules:

        The diff contains file paths and @@ hunk headers.

        For each issue:
        - determine the file_path
        - determine the line_number in the NEW file
        - report the exact changed line responsible

        Return ONLY valid JSON.
        Do not use markdown.
        Do not use code fences.
        Do not include explanations outside the JSON.

        JSON FORMAT:

        {{
            "summary": "Short summary of the review",
            "issues": [
                {{
                    "file_path": "path/to/file.py",
                    "line_number": 42,
                    "severity": "critical",
                    "category": "bug",
                    "comment": "Explain the issue and provide a concrete fix."
                }}
            ]
        }}

        If no meaningful issues are found, return EXACTLY:

        {{
            "summary": "No issues detected in the modified code.",
            "issues": []
        }}

        Diff:

        {diff_text}
        """

    try:
        response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
        )
    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            "summary": "AI review unavailable",
            "issues": []
        }
    
    raw_text = response.text.strip()
    raw_text = raw_text.replace('```json', '').replace('```', '').strip()

    result = json.loads(raw_text)

    return result
