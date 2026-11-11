# AI QA Journey

[![QA CI](https://github.com/AliHassan-creator/ai-qa-journey/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AliHassan-creator/ai-qa-journey/actions/workflows/ci.yml)

A practical five-week plan for moving from manual QA work to AI-enabled quality engineering. The program covers Python, Git, test automation, AI-assisted test design, MCP integrations, and evaluation of AI systems.

## Local setup

The project uses Python. Create and activate the folder virtual environment, then check the interpreter and package manager:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip --version
```

Git, VS Code, and the VS Code Python extension are used throughout the plan.

## Day 10: CI/CD with GitHub Actions

The [Day 10 guide](Day%2010%20-%20CI-CD%20with%20GitHub%20Actions/README.md) explains the workflow, Python matrix, API and browser jobs, scheduled run, artifacts, and status badge. GitHub Actions configuration is in [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Day 11: Prompting for test design

Start with the [Day 11 exercise](Day%2011%20-%20Prompting%20for%20Test%20Design/README.md), compare vague and structured prompts, and review the reusable [test-case generation prompt](qa-copilot/prompts/testcase_gen.md).

## Day 12: Advanced AI test design

The [Day 12 guide](Day%2012%20-%20Advanced%20AI%20Test%20Design/README.md) covers the five-prompt library, output-review checklist, and deterministic core validators.

## Day 1 checklist

- [ ] Create a branch and make a change.
- [ ] Open and merge a pull request.
- [ ] Practice resolving a merge conflict.
- [ ] Keep local secrets in `.env`; use `.env.example` as a placeholder template.
- [ ] Begin the `qa-copilot` scaffold.

## Day 1
- Installed Python, pip, Git, and VS Code tools.
- Connected the project to GitHub.
- Practiced Git version control.
