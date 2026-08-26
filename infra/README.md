# CS351 — Your Work

This is your personal, private repository for CS351. Only you and the
instructor can see it.

## Start here

1. Click **Code → Codespaces → Create codespace on main**.
2. VS Code asks **"Do you trust the authors of the files in this folder?"**
   Click **Trust Folder & Continue**. This is your own repository.
3. Wait for the environment to build. The first time takes about **three
   minutes**. It only happens once.
4. When the terminal is ready, type `begin` and press Enter. You should see a
   list of the assignments available to you. If you get `command not found`,
   the setup did not finish — say so in Discord rather than pressing on.

## The loop

Every assignment works the same way:

```bash
begin a1     # get the assignment
             # ... do the work ...
save         # hand it in
```

**Your work is not submitted until `save` has run.** Run it often — it is safe
to run as many times as you like, and it is what keeps your work from living
only inside a temporary container.

## Read these two, early

- **[How to Work on CS351](WORKFLOW.md)**
  — codespaces, `begin`, `save`, keeping your work between sessions, and what
  to do when something breaks. Short, and it answers most questions.
- **[How Homework Is Graded](GRADING.md)**
  — the same three criteria for every assignment. Comments on your work are
  advice, not deductions.

Both are already in this repository, refreshed every time `begin` runs.

## What is yours, and what is not

**Everything under `src/` is your work** — the assignments you fetch with
`begin`, and anything you add inside them. Nothing outside `src/` is.

Those other files come from the course, and they are refreshed every time you
run `begin`. That is deliberate: it means a correction to the grading document
or to these instructions reaches you without you doing anything. It also means
**changes you make to them will be replaced**, so if you want to keep notes,
keep them inside your assignment directory.

## If something goes wrong

Ask in Discord or in office hours. If `begin` or `save` reports that your
repository has an unfinished merge, do not try to fix it yourself — show your
instructor.
