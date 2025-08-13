#!/usr/bin/env python3
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
COPILOT = HERE / ".github" / "copilot"
RUNTIME = COPILOT / "runtime"

TAG_RE = re.compile(r"^(?P<prefix>[#@/])(?P<tag>[A-Za-z0-9_\-]+)$")


def load_prompt(name: str) -> dict:
    p = (COPILOT / "prompt-files" / name)
    with p.open() as f:
        return json.load(f)


def tag_to_file(ch: str, tag: str) -> Path:
    if ch == '#':
        return COPILOT / "context" / f"{tag}.md"
    if ch == '@':
        return COPILOT / "extensions" / f"{tag}.md"
    if ch == '/':
        return COPILOT / "commands" / f"{tag}.md"
    raise ValueError(f"Unknown tag prefix: {ch}")


def expand_body(body: str) -> str:
    out = []
    for line in body.splitlines():
        st = line.strip()
        m = TAG_RE.match(st)
        if m:
            ch = m.group("prefix")
            tag = m.group("tag")
            path = tag_to_file(ch, tag)
            out.append(path.read_text() if path.exists() else f"<!-- missing tag {st} -->")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    for mode_file in (COPILOT / "modes").glob("*.yaml"):
        name = mode_file.stem
        text = mode_file.read_text()
        prompt = None
        for ln in text.splitlines():
            if ln.strip().startswith("prompt_file:"):
                prompt = ln.split(":", 1)[1].strip()
                break
        if not prompt:
            continue
        prompt_json = load_prompt(prompt)
        body = expand_body(prompt_json.get("body", ""))
        out_path = RUNTIME / f"{name}.md"
        out_path.write_text(body)
        print(f"Generated {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
