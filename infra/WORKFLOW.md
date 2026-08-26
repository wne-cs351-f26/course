# How to Work on CS351

Everything in this course runs through the same three-step loop, and it does
not change from one assignment to the next.

```bash
begin a1     # get the assignment
             # ... do the work ...
save         # hand it in
```

The rest of this document is what those steps actually do, and what to do when
something does not go the way it should.

## Your codespace

Your work happens in a **GitHub Codespace** — a development environment that
runs in the cloud and opens in your browser, already set up with everything
this course needs. You do not install anything on your own machine.

### Starting one the first time

1. Open your CS351 repository on GitHub.
2. Click the green **Code** button, choose the **Codespaces** tab, then
   **Create codespace on main**.
3. Wait. The first build takes several minutes because it is downloading and
   configuring the whole environment. This is normal and it only happens once.
4. When it finishes you will see:

   ```
   CS351 environment ready. Run 'begin' to list assignments.
   ```

If you do not see that line, something went wrong with the setup — say so in
Discord rather than pressing on, because `begin` and `save` will not work.

### Coming back to it

**Reopen the codespace you already have. Do not create a second one.**

Go to <https://github.com/codespaces>, or use the same **Code → Codespaces**
menu on your repository, and click the codespace that is already listed.
Reopening is fast — the slow first build does not happen again.

Creating a second codespace is not fatal, but it gives you two separate copies
of your work that know nothing about each other, and sorting that out later is
genuinely annoying. One codespace.

### Stopping it

A codespace **stops on its own** after a while with no activity, and you can
stop it yourself from <https://github.com/codespaces>.

Stopping is not losing. A stopped codespace keeps all of its files and starts
again where you left off.

The reason to care is that codespaces are metered. GitHub gives you a monthly
allowance of core-hours — 120 on the free tier, 180 once your Student
Developer Pack verification comes through — and a running codespace spends it
whether or not you are typing. Stopping one you are done with costs you
nothing and keeps the allowance for when you need it.

## Getting an assignment

```bash
begin a1
```

That copies the starter files for `a1` into a new `src/a1/` directory in your
repository, and records a pristine copy of them so it is always possible to
see what you changed.

Run `begin` with no arguments to see what is available:

```bash
begin
```

**An assignment you expect to see may not be listed.** Assignments appear only
once they are released. If one is missing, it has not been released yet — it
is not something wrong with your setup.

`begin` will refuse to overwrite work you have already started. If you really
want to throw away your changes and start that assignment over, `begin -f a1`
does it — but it discards your edits to those files permanently, so be sure.

## Doing the work

Your assignment's files are in the directory `begin` created — `src/a1/` for
assignment 1. Edit them like any other files, in the editor on the left.

You will need a terminal for most questions. If one is not already open,
**Terminal → New Terminal**, or ``Ctrl-` ``. Most assignments ask you to be
in a particular directory when you run things, so read the instructions.

Written answers usually go in the assignment's `README.md`, in the blocks
marked `ANSWER`. The assignment will tell you.

## Saving and submitting

```bash
save
```

or, if you want to leave yourself a note about what you did:

```bash
save finished step 7
```

`save` commits everything in your repository and pushes it to GitHub. That is
all it does, and it is the only thing that submits your work.

**Your work is not submitted until `save` has run.** Editing files in your
codespace does not submit anything. Neither does the editor's own autosave —
that saves to the container your codespace is running in, which is not the
same as saving to GitHub.

Run it often. It is safe to run as many times as you like, and there is no
penalty for saving work that is not finished. A good habit is to run it every
time you finish a step. What gets graded is whatever is in GitHub at the
deadline, so the more often you save, the less you can lose.

## Between sessions — the part people learn the hard way

Your codespace is a computer somewhere else, and your files live on it until
`save` pushes them to GitHub.

A stopped codespace keeps your files. But a codespace can also be **deleted** —
by you, or by GitHub after a long enough stretch of not being used — and when
it is deleted, anything in it that was never pushed goes with it. There is no
recovering that. Nobody has a copy, because a copy is exactly what `save`
makes.

So: **run `save` before you stop working.** Not because you are submitting —
you can save a hundred times before the deadline — but because until you do,
your work exists in exactly one place, and that place is temporary.

If you finish a session and you are not sure whether you saved, run `save`
again. Running it twice costs nothing.

## When something goes wrong

**`begin` or `save` reports an unfinished merge.** Stop. Do not try to fix it.
Show your instructor the message — in office hours, or as a screenshot in
Discord. Your work is not lost; it is still on disk. But running the command
again will not fix it, and the usual fixes people find by searching can make
it worse.

**`save` reports an error you do not understand.** Take a screenshot that
includes the error text and bring it to office hours or Discord. The exact
message matters, so a screenshot beats a description.

**`begin` warns that it could not refresh course materials.** That means the
network was unavailable. It continues with what is already on disk, which is
usually fine. If the assignment then looks wrong or incomplete, say so.

**Anything else.** Ask in Discord or come to office hours. Being stuck on the
tooling is not the same as being stuck on the material, and it is not
something to spend an evening on alone.

## Which files are yours

Your repository holds two kinds of file.

**Your work lives under `src/`.** `begin a1` creates `src/a1/`, and everything
in it is yours: the handout you write answers into, the files you edit, anything
you add. Nothing the course does will ever overwrite it. The one exception is
`begin -f`, which you have to ask for by name, and which tells you what it is
about to discard.

**Everything else belongs to the course** — `README.md`, `GRADING.md`, this
file, `.gitignore`, and the `.devcontainer` and `.vscode` directories. Every
time you run `begin`, those are refreshed from the course repository. If I fix a
mistake in the grading document, you get the fix automatically. If you edit one
of them, your edit is replaced the next time you run `begin`.

Nothing is lost when that happens: `save` has already committed your work, so
the old version stays in your repository's history.

If your repository is in a state that cannot be written to safely — an
unfinished merge, most likely — `begin` says so and skips the refresh rather
than making things worse. Your own work is never touched by it.

## See also

- [GRADING.md](GRADING.md) — how every assignment is scored.
- The syllabus, on Kodiak, for due dates, the grace period, and course
  policies.
