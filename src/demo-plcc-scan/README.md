# CS351 - Demo: `plcc-scan` and the tie-break

**Nothing here is graded and nothing here is submitted.** This is a sandbox.
Break it, edit the files, delete things. When you want it back the way it
started:

```bash
begin -f demo-plcc-scan
```

That replaces this whole directory with a fresh copy, discarding whatever you
did to it. There is no way to lose anything that matters, because nothing in
here counts.

## What it is for

We worked through this on the board. This is the same thing with the tool in
front of you, so you can run it yourself instead of watching me run it.

It is also the mechanism **A1 question 3 asks you to explain** — steps 6, 7 and
10 all turn on it. Play with it here first, where being wrong is free.

## Before you run anything — be in the right directory

`begin` put these files in `src/demo-plcc-scan/` inside your repository. Every command
below assumes that is where your terminal is:

```bash
cd src/demo-plcc-scan
```

Three things depend on it, and all three fail in confusing ways rather than
obvious ones:

- **`-s spec.plcc` is a relative path.** From anywhere else, that file does not
  exist and you get an error about the specification, not about your directory.
- **`plcc-ng/` is written into whatever directory you run from.** It is the build
  cache, and it belongs next to the specification it was built from.
- **The sticky `-s` is remembered inside that `plcc-ng/`**, so a different
  directory remembers a different specification.

If a command surprises you, check `pwd` before you check anything else.

## The files

| File | What it is |
| --- | --- |
| `spec.plcc` | Comma-separated numbers. The default specification. |
| `input.txt` | `1, 2, 3` in a file. |
| `tie1.plcc` | Three rules that all match. Longest wins. |
| `tie2.plcc` | Two rules, same length. First wins — and one rule can never fire. |
| `tie3.plcc` | `tie2.plcc` with the two rules swapped. |

`-s` points `plcc-scan` at a specification other than `spec.plcc`.

> **`-s` is sticky.** Once you pass it, it is remembered for later commands
> until you change it. So after `-s tie1.plcc`, a bare `plcc-scan` still uses
> `tie1.plcc` — not `spec.plcc`. Pass `-s` explicitly every time below and it
> cannot surprise you.

## 1 — Run it, and read what it prints

```console
$ echo "1, 2, 3" | plcc-scan -s spec.plcc
-:1:1 NUM '1'
-:1:2 COMMA ','
-:1:4 NUM '2'
-:1:5 COMMA ','
-:1:7 NUM '3'
```

Each line is **source:line:column, token name, lexeme in quotes**. The `-` in
the source position means the input did not come from a file. Hand it a file
and the name appears instead:

```console
$ plcc-scan -s spec.plcc input.txt
input.txt:1:1 NUM '1'
```

Now look at what is **not** there. The spaces matched `skip WHITESPACE`, so
they were consumed and nothing was emitted. `skip` and `token` rules both have
to match; only one of them produces output.

## 2 — Longest match wins

`tie1.plcc`:

```
skip WHITESPACE '\s+'
token HI 'hi'
token WORD '\w+'
token ANY '.+'
```

Three rules can match at the start of `hi there`. Before you run it, decide
which one you think wins. Then use `-t`, which prints the candidate table and
stars the winner:

```console
$ echo "hi there" | plcc-scan -t -s tie1.plcc

Candidates:
#  Type   Name  Pattern  Len  Match
2  token  HI    'hi'     2    'hi'
3  token  WORD  '\w+'    2    'hi'
4  token  ANY   '.+'     8*   'hi there'
* longest match wins; ties broken by earliest rule (#)
```

`ANY` wins with 8 characters — even though `HI` is written first and matches
perfectly well. **Length beats order.**

## 3 — Among equal-length matches, the first rule wins

`tie2.plcc`:

```
skip WHITESPACE '\s+'
token WORD '\w+'
token FROM 'from'
```

```console
$ echo "from" | plcc-scan -t -s tie2.plcc

Candidates:
#   Type   Name  Pattern  Len  Match
2*  token  WORD  '\w+'    4    'from'
3   token  FROM  'from'   4    'from'
* longest match wins; ties broken by earliest rule (#)
```

Both match. Both are four characters long. The star is on rule 2, so `WORD`
wins.

Now the part worth sitting with: **`FROM` is never emitted. Not for this input
— for any input.** Every string `FROM` could match, `WORD` also matches, at the
same length, from an earlier line. The rule is dead and nothing tells you so.
There is no error, no warning. The candidate table is the only place it is
visible.

**The rule to remember, and the one A1 question 3 needs:** put literal words
*above* the general patterns with `+` or `*`, or your reserved words will never
fire.

## 4 — Prove it by swapping them

`tie3.plcc` is `tie2.plcc` with the two lines in the other order:

```console
$ echo "from" | plcc-scan -t -s tie3.plcc

Candidates:
#   Type   Name  Pattern  Len  Match
2*  token  FROM  'from'   4    'from'
3   token  WORD  '\w+'    4    'from'
* longest match wins; ties broken by earliest rule (#)
```

The star moved. Same input, same two rules, one line swapped.

## Now break it yourself

No answers below, and nothing to hand in. Predict first, then run with `-t` and
find out.

- Add `token FOUR '....'` to `tie2.plcc`. Does it change who wins on `from`?
  What about on a five-letter word?
- Delete the `skip WHITESPACE` line from `tie1.plcc` and run it again. What
  happens at the end of the line, and why?
- In `spec.plcc`, add `token ID '\w+'` **above** `token NUM '\d+'`. What does
  `1, 2, 3` scan as now? Move it below and try again.
- Write a specification where a rule you wrote can never fire, and confirm it
  with `-t` before you convince yourself it is true.
- Feed `plcc-scan` something with no rule to match it. Read the error. It is
  not the scanner failing — it is the scanner telling you your specification
  does not describe this input.

Reset whenever you want with `begin -f demo-plcc-scan`.
