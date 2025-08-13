import re
from typing import List, Optional, Tuple

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


def _infer_type_and_scope(files: List[str], diff: str) -> Tuple[str, Optional[str]]:
    """Infer Conventional Commit type and optional scope from changed files and diff.

    Types considered: feat, fix, docs, style, refactor, perf, test, build, ci, chore.
    Scope is the top-level folder of the first file (if any).
    """
    type_priority = [
        "fix",
        "feat",
        "docs",
        "test",
        "refactor",
        "perf",
        "ci",
        "build",
        "style",
        "chore",
    ]

    def top_scope(path: str) -> Optional[str]:
        parts = path.split("/")
        return parts[0] if parts else None

    scope = top_scope(files[0]) if files else None

    # Heuristics by path
    path_types = set()
    for f in files:
        if f.startswith("tests/") or "/tests/" in f or re.search(r"(^|/)test_", f):
            path_types.add("test")
        if f.endswith(('.md', '.rst')) or f.startswith('docs/'):
            path_types.add("docs")
        if f.startswith('.github/'):
            path_types.add("ci")
        if f.endswith(('pyproject.toml', 'setup.cfg', 'setup.py')) or 'Dockerfile' in f:
            path_types.add("build")
        if re.search(r"\.(css|scss|less|prettierrc|editorconfig)$", f):
            path_types.add("style")

    # Heuristics by diff content
    if re.search(r"\bfix(e[ds])?|bug\b", diff, re.IGNORECASE):
        path_types.add("fix")
    if re.search(r"\bperf|optimi(s|z)e|performance\b", diff, re.IGNORECASE):
        path_types.add("perf")
    if re.search(r"\brefactor|rename\b", diff, re.IGNORECASE):
        path_types.add("refactor")
    if re.search(r"^\+\s*def |^\+\s*class ", diff, re.MULTILINE):
        path_types.add("feat")

    # Choose highest priority found, fallback to chore
    for t in type_priority:
        if t in path_types:
            return t, scope
    return "chore", scope


def generate_commit_message(diff: str, conventional: bool = False) -> str:
    files = summarize_diff(diff)
    if not files:
        return "chore: update repository"
    if len(files) == 1:
        subject_core = f"update {files[0]}"
    else:
        subject_core = f"update {len(files)} files: {', '.join(files[:3])}{'…' if len(files) > 3 else ''}"
    if conventional:
        ctype, scope = _infer_type_and_scope(files, diff)
        scope_str = f"({scope})" if scope and scope not in {None, '.', ''} else ""
        subject = f"{ctype}{scope_str}: {subject_core}"
    else:
        subject = subject_core.capitalize()

    # Basic body from diff stats
    added = len([l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')])
    removed = len([l for l in diff.splitlines() if l.startswith('-') and not l.startswith('---')])
    body = f"Changes: +{added} -{removed} lines\n\nFiles:\n- " + "\n- ".join(files)
    return f"{subject}\n\n{body}\n"
