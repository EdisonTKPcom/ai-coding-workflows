import re
from typing import List

CONVENTIONAL_TYPES = [
    "feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"
]


def summarize_diff(diff: str, max_lines: int = 10) -> List[str]:
    # Very light heuristic summary from diff headers
    lines = diff.splitlines()
    files = []
    for ln in lines:
        if ln.startswith("+++ b/"):
            files.append(ln[6:])
    files = list(dict.fromkeys(files))  # dedupe preserving order
    files = files[:max_lines]
    return files


def generate_commit_message(diff: str, conventional: bool = False) -> str:
    files = summarize_diff(diff)
    if not files:
        return "chore: update repository"
    if len(files) == 1:
        subject_core = f"update {files[0]}"
    else:
        subject_core = f"update {len(files)} files: {', '.join(files[:3])}{'…' if len(files) > 3 else ''}"
    if conventional:
        # Default to chore type; could be enhanced with heuristics
        subject = f"chore: {subject_core}"
    else:
        subject = subject_core.capitalize()

    # Basic body from diff stats
    added = len([l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')])
    removed = len([l for l in diff.splitlines() if l.startswith('-') and not l.startswith('---')])
    body = f"Changes: +{added} -{removed} lines\n\nFiles:\n- " + "\n- ".join(files)
    return f"{subject}\n\n{body}\n"
