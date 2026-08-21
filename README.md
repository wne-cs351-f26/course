# CS351 Course Repository

Public. Holds assignment starter code and the student CLI.

- `src/<assignment>/` — starter files. `begin <assignment>` copies these
  into a student's repository.
- `bin/` — the `begin` and `save` commands.
- `template/` — the skeleton seeded into each student repository.

**No solutions here.** Solutions live in the instructor's private
repository. Anything committed here is world-readable.

## Releasing assignments

`released.txt` controls what students can fetch. `begin` lists only what
appears there, and refuses anything in `src/` that does not — so a student
cannot start work on material that may still change before it is assigned.

To release something: add its line, commit, push. `begin` pulls on every run,
so it takes effect immediately with no action from students.

Note that this repository is public, so an unreleased assignment is still
*readable* on github.com. The manifest prevents students from starting work
against a moving target; it is not a concealment mechanism. Anything that must
stay unseen — solutions especially — belongs in the instructor's private
repository until release.

## Staging changes

`begin` honours `BEGIN_BRANCH` (default `main`). To test a risky change,
push it to a branch, set `BEGIN_BRANCH` in the rehearsal repository, verify,
then merge to `main`.
