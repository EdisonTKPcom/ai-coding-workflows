from pathlib import Path


def _write(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(content)


def generate_instruction_scaffold(target_dir: Path) -> None:
    """Generate the AI Standards scaffold under the given target directory.

    Expected structure (relative to target_dir):
      instructions.md
      prompt-files/*.json
      context/*.md
      extensions/*.md
      commands/*.md
      toolsets/*.yaml
      modes/*.yaml
      mcp/*.yaml
      runtime/ (output-only)
    """
    # Base files
    _write(target_dir / "instructions.md", """# AI House Rules\n\n- Use tests for public behavior changes.\n- Follow security best practices.\n- Prefer readability.\n""")

    # Sample prompt file
    _write(
        target_dir / "prompt-files" / "pr_risk_review.json",
        """{
  "title": "PR Risk Review",
  "inputs": ["diff", "risks?"],
  "body": "Review this diff for security, perf, and data-loss risks.\n#repo\n#security\n@refactor\n/risk_review"
}
""",
    )

    # Context, extensions, commands
    _write(
        target_dir / "context" / "repo.md",
        """## Repository Overview\n\nSummarize the repository's purpose, modules, and critical paths.\n""",
    )
    _write(
        target_dir / "context" / "security.md",
        """## Security Rules\n\n- No secrets in code.\n- Validate inputs.\n- Least privilege.\n""",
    )
    _write(
        target_dir / "extensions" / "refactor.md",
        """## Refactor Checklist\n\n- Remove dead code.\n- Reduce duplication.\n- Keep functions small.\n""",
    )
    _write(
        target_dir / "commands" / "risk_review.md",
        """## Risk Triage Steps\n\n1. Identify data-loss and security risks.\n2. Estimate impact and likelihood.\n3. Propose mitigations.\n""",
    )

    # Toolsets, modes, mcp
    _write(
        target_dir / "toolsets" / "default.yaml",
        """tools:\n  - name: shell\n  - name: fs\n  - name: git\n  - name: http\n""",
    )
    _write(
        target_dir / "modes" / "reviewer.yaml",
        """name: reviewer\nprompt_file: pr_risk_review.json\ncontext: [repo, security]\nextensions: [refactor]\ncommands: [risk_review]\n""",
    )
    _write(
        target_dir / "modes" / "coder.yaml",
        """name: coder\nprompt_file: pr_risk_review.json\ncontext: [repo]\nextensions: []\ncommands: []\n""",
    )
    _write(
        target_dir / "mcp" / "servers.yaml",
        """servers:\n  - name: filesystem\n    url: mcp://filesystem\n  - name: git\n    url: mcp://git\n""",
    )

    # runtime dir placeholder
    (target_dir / "runtime").mkdir(parents=True, exist_ok=True)
    _write(target_dir / "runtime" / ".gitkeep", "")
