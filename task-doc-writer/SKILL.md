---
name: task-doc-writer
description: Write a Markdown document for the current task under a project-level .docs folder. Use when the user asks to document, summarize, record, or archive the current task, implementation, file changes, maintenance work, or completion notes; especially when they ask for a task document, work log, change summary, or project documentation after coding.
---

# Task Doc Writer

## Overview

Create a concise Markdown task document in the current project's `.docs` directory. The document should summarize what was done and, when files changed, record which workspace files were touched and why.

## Workflow

1. Identify the project root.
   - Prefer the repository root from `git rev-parse --show-toplevel` when available.
   - Otherwise use the current workspace root or current working directory.
2. Read the computer's current local date immediately before creating the document.
   - Run `python scripts/current_date.py` from this skill directory.
   - Use the returned `filename_date` for the filename and `document_date` for the date written inside the document.
   - Never infer the date from the conversation, an example filename, model knowledge, or a previously generated document.
   - If the script cannot run, query the operating system directly: use PowerShell `Get-Date -Format 'yyMMdd'` and `Get-Date -Format 'yyyy-MM-dd'` on Windows, or `date +%y%m%d` and `date +%F` on Unix-like systems.
   - Treat the operating system result as authoritative even when it conflicts with dates mentioned elsewhere in the context, unless the user explicitly requests a historical or custom date.
3. Ensure a `.docs` directory exists directly under the project root.
4. Choose a clear document title from the user's request or the completed task.
5. Create a Markdown file named `<filename_date>-title.md`.
   - Replace `YYMMDD` with the script's `filename_date` value.
   - Keep the title short and filesystem-safe.
   - Use lowercase hyphenated English titles when no Chinese title was requested.
   - If the target filename already exists, append `-2`, `-3`, etc.
6. Write the task document in Markdown and use the script's `document_date` value for its date field.
7. Verify that project file paths in the document are workspace-relative and do not include a drive letter, user home path, or absolute computer path.

## System Date Helper

Run the bundled helper before every document creation:

```shell
python scripts/current_date.py
```

It returns JSON in this shape:

```json
{
  "filename_date": "YYMMDD from the system clock",
  "document_date": "YYYY-MM-DD from the system clock",
  "generated_at": "local ISO 8601 timestamp"
}
```

Do not copy the example values. Always use the values from the current invocation.

## Document Content

Use Chinese section headings by default when the user is working in Chinese. Use this structure unless the user requests a different one:

```markdown
# Title

Date: <document_date from current_date.py>

## Task Summary

Summarize the task in 2-5 bullets or short paragraphs.

## Completed Work

List the concrete work completed.

## Involved Files

| File | Reason |
| --- | --- |
| path/from/workspace.ext | Explain why this file was created, edited, moved, deleted, or inspected. |

## Validation

Record checks performed, commands run, or note when validation was not run.
```

If no project files changed, keep the `Involved Files` section and state that no project files were modified.

## File Change Rules

- When the task changed file contents, include every created, edited, moved, or deleted project file that is relevant to the task.
- For each file, explain the reason for the operation, not just the mechanical change.
- Include files read or inspected only when they materially shaped the work and the user would benefit from knowing that context.
- Prefer `git status --short` and `git diff --name-only` to discover changed files when the project is a Git repository.
- Also include files created outside Git tracking if they are part of the task and live under the workspace.
- Do not invent validation. If tests or checks were not run, state that briefly.

## Path Rules

- Write paths relative to the workspace or project root, for example `src/main.ts` or `.docs/<filename_date>-task-doc.md`.
- Do not write paths like `C:\Users\...`, `/Users/...`, or any machine-specific absolute path inside the task document.
- If a referenced artifact is outside the workspace, describe it by role or filename only unless the user explicitly asks for its absolute location.
