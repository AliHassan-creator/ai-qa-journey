# Day 1 Deliverable: Git and GitHub Setup

## Objective

Show the repository setup, Git and GitHub workflow, merge-conflict practice,
secret-handling files, and the initial QA-Copilot project skeleton completed for
Day 1 of the learning plan.

## Evidence in this repository

| Day 1 requirement | Evidence | Status |
|---|---|---|
| Create a repository and use Git | This Git repository and its commit history | Present; history reviewed on 2026-10-26 |
| Create a branch, open a pull request, and merge it | Merged PR #1 added the pull request walkthrough; merged PR #2 updated the README. See the merge commits in `git log`. | Present in local history |
| Practice resolving a merge conflict | [`conflict-practice.txt`](../conflict-practice.txt) | Present; contains the recorded resolution `Status: approved` |
| Add `.gitignore` and `.env.example` | [`.gitignore`](../.gitignore) and [`.env.example`](../.env.example) | Present; `.env` is ignored and the example contains blank placeholders |
| Start the QA-Copilot skeleton | [`qa-copilot/README.md`](../qa-copilot/README.md) and its `core`, `runner`, `prompts`, `samples`, and `tests` folders | Present |
| Keep a reusable pull request walkthrough | [`docs/day1-pull-request-walkthrough.md`](../docs/day1-pull-request-walkthrough.md) | Present |

## Verify locally

From the repository root in PowerShell:

```powershell
git status --short --branch
git log --oneline --decorate -5
git rev-list --count HEAD
Get-Content .gitignore
Get-Content .env.example
Get-ChildItem qa-copilot -Recurse
```

The commit history contains the merged pull request work. The working tree may
also contain later untracked learning files; review `git status` before staging
anything. Do not add a real `.env` file or credentials to Git.

## Scope and remaining evidence

This folder is the Day 1 evidence index. The repository-wide Git history and
configuration remain in their original locations so existing paths and history
are preserved. The existing `Day1.png` screenshot contains unrelated console
output as well as Git commands, so it is not presented as clean Day 1 evidence.

The workbook's Day 1 deliverable asks for a repository link with at least five
commits and one merged pull request. Local history shows merged pull request
work; confirm the live GitHub repository URL and pull request pages when
presenting this deliverable externally.
