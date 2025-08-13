# AI Standards Repository

This repository defines the **organization-wide AI usage standards** for GitHub Copilot, Agentic AI workflows, and MCP server configurations.

It provides **Prompt Files**, **Instructions**, **Tool Sets**, **Modes**, and **MCP Servers**, along with a **Generator** that composes runtime-ready instruction files from reusable components.

---

## 📂 Repository Structure

```
.github/
└── copilot/
    ├── instructions.md           # House rules & policies for AI
    ├── prompt-files/              # JSON prompt templates with tag refs (#, @, /)
    ├── context/                   # Reusable context blocks (#tag)
    ├── extensions/                # Optional add-ons (@tag)
    ├── commands/                  # Actionable commands (/tag)
    ├── toolsets/                   # Tool configuration (shell, git, http, etc.)
    ├── modes/                      # Predefined AI modes (reviewer, coder, etc.)
    ├── mcp/                        # MCP server configurations
    └── runtime/                    # Auto-generated instructions per mode (from CI)
schemas/                            # JSON Schema definitions for validation
scripts/                            # Automation scripts (generate_instructions.py, validate.py)
.github/workflows/                  # CI workflows for validation & generation
.copilot/                           # Minimal mirror for tools expecting this folder
README.md                           # This file
```

---

## 🧩 Core Components

### 1. Prompt Files (`.github/copilot/prompt-files/`)
Reusable, parameterized AI prompts in JSON format.  
Use **tag syntax** to include extra content:

- **Add context** → `#tag` (from `/context`)
- **Add extensions** → `@tag` (from `/extensions`)
- **Add commands** → `/command` (from `/commands`)

**Example:**
```json
{
  "title": "PR Risk Review",
  "inputs": ["diff", "risks?"],
  "body": "Review this diff for security, perf, and data-loss risks.\n#repo\n#security\n@refactor\n/risk_review"
}
```

---

### 2. Instructions (`.github/copilot/instructions.md`)
Defines your **house rules** and default behavior for Copilot & AI agents:
- Code style
- Test coverage requirements
- Security rules
- Project glossary

---

### 3. Tool Sets (`.github/copilot/toolsets/`)
Lists allowed tools & capabilities for the AI, e.g.:
```yaml
tools:
  - name: shell
  - name: fs
  - name: git
  - name: http
```

---

### 4. Modes (`.github/copilot/modes/`)
Bundles a default prompt file, context, and extensions into **ready-to-run modes**:
- `reviewer.yaml` → uses `PR_Risk_Review` + `#repo` + `@refactor`
- `coder.yaml` → uses `Test_Generator` + `#repo` + `@docs`

---

### 5. MCP Servers (`.github/copilot/mcp/`)
Configuration for [Model Context Protocol](https://modelcontextprotocol.io/) servers:
```yaml
servers:
  - name: filesystem
    url: mcp://filesystem
  - name: git
    url: mcp://git
```

---

## ⚙️ CI Automation

The `.github/workflows/ai-standards-validate.yml` workflow:

1. **Validates** all prompt files, instructions, tool sets, and modes against their JSON Schemas.
2. **Generates** runtime instructions by expanding tags (`#/@//`) into full content.
3. Uploads generated instruction files to `.github/copilot/runtime/`.

---

## 🚀 Usage

### In a single repo
1. Copy `.github/copilot/` from this repo.
2. Adjust `context/`, `extensions/`, and `commands/` for project-specific needs.
3. Commit changes — CI will validate and generate runtime instructions.

### Organization-wide
- Keep this repo as **source of truth**.
- Use as a **submodule** or **template** in other repos.
- Optionally, add a **sync workflow** that pulls updates from this repo into all project repos.

---

## 📌 Example Flow

1. Dev opens a PR → GitHub Copilot Reviewer mode triggers.
2. Reviewer prompt uses:
   - `#repo` → project overview
   - `#security` → security rules
   - `@refactor` → coding cleanup checklist
   - `/risk_review` → risk triage instructions
3. Output is consistent, enforceable, and traceable.

---

## 📜 License
This repo is intended for **internal organizational use**. Adapt and redistribute under your company’s licensing policies.
