#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft7Validator
import yaml

ROOT = Path(__file__).resolve().parents[1]
COP = ROOT / ".github" / "copilot"
SCHEMAS = ROOT / "schemas"


def validate_prompts() -> int:
    schema = json.loads((SCHEMAS / "prompt-file.schema.json").read_text())
    validator = Draft7Validator(schema)
    errors = 0
    for p in (COP / "prompt-files").glob("*.json"):
        data = json.loads(p.read_text())
        for err in validator.iter_errors(data):
            print(f"Prompt {p.name}: {err.message}")
            errors += 1
    return errors


def validate_modes() -> int:
    schema = json.loads((SCHEMAS / "mode.schema.json").read_text())
    validator = Draft7Validator(schema)
    errors = 0
    for p in (COP / "modes").glob("*.yaml"):
        data = yaml.safe_load(p.read_text())
        for err in validator.iter_errors(data):
            print(f"Mode {p.name}: {err.message}")
            errors += 1
    return errors


def validate_toolsets() -> int:
    schema = yaml.safe_load((SCHEMAS / "toolset.schema.yaml").read_text())
    validator = Draft7Validator(schema)
    errors = 0
    for p in (COP / "toolsets").glob("*.yaml"):
        data = yaml.safe_load(p.read_text())
        for err in validator.iter_errors(data):
            print(f"Toolset {p.name}: {err.message}")
            errors += 1
    return errors


def validate_mcp() -> int:
    schema = yaml.safe_load((SCHEMAS / "mcp.schema.yaml").read_text())
    validator = Draft7Validator(schema)
    errors = 0
    mcp = yaml.safe_load((COP / "mcp" / "servers.yaml").read_text())
    for err in validator.iter_errors(mcp):
        print(f"MCP servers: {err.message}")
        errors += 1
    return errors


def validate_instructions() -> int:
    # We allow markdown instructions; just assert file exists and non-empty.
    md = COP / "instructions.md"
    if not md.exists() or not md.read_text().strip():
        print("instructions.md missing or empty")
        return 1
    # Optional JSON form validated if present.
    j = COP / "instructions.json"
    if j.exists():
        schema = json.loads((SCHEMAS / "instructions.schema.json").read_text())
        validator = Draft7Validator(schema)
        data = json.loads(j.read_text())
        errs = 0
        for err in validator.iter_errors(data):
            print(f"Instructions JSON: {err.message}")
            errs += 1
        return errs
    return 0


def main() -> int:
    errs = 0
    errs += validate_prompts()
    errs += validate_modes()
    errs += validate_toolsets()
    errs += validate_mcp()
    errs += validate_instructions()
    if errs:
        print(f"Validation failed: {errs} errors")
        return 1
    print("Validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
