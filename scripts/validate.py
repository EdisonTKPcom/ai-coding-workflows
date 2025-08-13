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


def main() -> int:
    errs = 0
    errs += validate_prompts()
    errs += validate_modes()
    errs += validate_toolsets()
    if errs:
        print(f"Validation failed: {errs} errors")
        return 1
    print("Validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
