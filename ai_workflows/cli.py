#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path
from .generator import generate_instruction_scaffold
from .git_ai import generate_commit_message

REPO_ROOT = Path(__file__).resolve().parents[1]


def cmd_generate(args: argparse.Namespace) -> int:
    target = Path(args.output) if args.output else REPO_ROOT / "workflows"
    target.mkdir(parents=True, exist_ok=True)
    generate_instruction_scaffold(target)
    print(f"Scaffold created at {target}")
    return 0


def cmd_generate_standards(args: argparse.Namespace) -> int:
    target = Path(args.output) if args.output else REPO_ROOT / ".github" / "copilot"
    target.mkdir(parents=True, exist_ok=True)
    generate_instruction_scaffold(target)
    print(f"AI Standards scaffold created at {target}")
    return 0


def cmd_ai_commit(args: argparse.Namespace) -> int:
    # Get git diff for staged changes
    try:
        diff = subprocess.check_output(["git", "--no-pager", "diff", "--staged"], text=True)
    except subprocess.CalledProcessError:
        print("No staged changes or git not initialized.")
        return 1
    message = generate_commit_message(diff, conventional=args.conventional)
    if args.print:
        print(message)
        return 0
    # Create commit
    subprocess.check_call(["git", "commit", "-m", message])
    print("Committed with AI-generated message.")
    return 0


def cmd_install_hook(args: argparse.Namespace) -> int:
    hooks_dir = REPO_ROOT / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "prepare-commit-msg"
    hook_content = """#!/usr/bin/env bash
# Auto-generate a commit message using aiwf if none provided
set -euo pipefail
COMMIT_MSG_FILE="$1"
COMMIT_SOURCE="${2-}"
SHA1="${3-}"
# Only run for normal commits where message is empty template
if [ -n "$COMMIT_SOURCE" ] && [ "$COMMIT_SOURCE" != "message" ]; then
  exit 0
fi
if [ -s "$COMMIT_MSG_FILE" ]; then
  exit 0
fi
if command -v aiwf >/dev/null 2>&1; then
  MSG=$(aiwf ai-commit --print --conventional || true)
  if [ -n "$MSG" ]; then
    echo "$MSG" > "$COMMIT_MSG_FILE"
  fi
fi
exit 0
"""
    hook_path.write_text(hook_content)
    os.chmod(hook_path, 0o755)
    print(f"Installed git hook at {hook_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aiwf", description="AI Coding Workflows CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Create scaffolding for workflows")
    g.add_argument("--output", "-o", help="Target directory for scaffold")
    g.set_defaults(func=cmd_generate)

    gs = sub.add_parser("generate-standards", help="Create .github/copilot AI Standards scaffold")
    gs.add_argument("--output", "-o", help="Target directory (defaults to .github/copilot)")
    gs.set_defaults(func=cmd_generate_standards)

    c = sub.add_parser("ai-commit", help="Generate and/or perform an AI-assisted git commit")
    c.add_argument("--print", action="store_true", help="Print the message instead of committing")
    c.add_argument("--conventional", action="store_true", help="Format as Conventional Commit")
    c.set_defaults(func=cmd_ai_commit)

    h = sub.add_parser("install-hook", help="Install a prepare-commit-msg hook for AI commit messages")
    h.set_defaults(func=cmd_install_hook)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
