---
name: summary_git
description: Summarizes changes since the last git commit, appends them to git_history.md, and commits/pushes all changes to GitHub. Use when the user wants to: (1) Record project changes to a history file, (2) Commit and push all local changes to GitHub, (3) Generate a summary of recent modifications
---

# summary_git

## Usage

Run this skill when user wants to record git changes to history and push to GitHub.

## Workflow

1. **Check git status**: Run `git status` to see all changes
2. **Get diff**: Run `git diff HEAD` to see detailed changes
3. **Read existing git_history.md**: If it exists, read its content first
4. **Generate summary**: Create a summary with:
   - Date (YYYY-MM-DD format)
   - Files changed (list each file)
   - Changes summary (additions/deletions)
5. **Append to git_history.md**: Add new entry at the top of the file
6. **Stage all changes**: `git add -A`
7. **Commit**: Create commit with message describing changes
8. **Push**: `git push` to push to remote

## Output Format

```markdown
## YYYY-MM-DD

### Changes
- file1.py: Added feature X, fixed bug Y
- file2.py: Updated configuration

### Stats
- X files changed, Y insertions(+), Z deletions(-)
```

## Example Commit Message

Format: `Update: [brief description]`

Example: `Update: Add new feature and fix configuration`
