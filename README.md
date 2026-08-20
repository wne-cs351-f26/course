# CS351 Course Repository

Public. Holds assignment starter code and the student CLI.

- `src/<assignment>/` — starter files. `begin <assignment>` copies these
  into a student's repository.
- `bin/` — the `begin` and `save` commands.
- `template/` — the skeleton seeded into each student repository.

**No solutions here.** Solutions live in the instructor's private
repository. Anything committed here is world-readable.

## Staging changes

`begin` honours `BEGIN_BRANCH` (default `main`). To test a risky change,
push it to a branch, set `BEGIN_BRANCH` in the rehearsal repository, verify,
then merge to `main`.
