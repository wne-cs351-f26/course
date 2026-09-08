# CS351 - Demo: `plcc-parse`, grammars, and the parse tree

**Nothing here is graded and nothing here is submitted.** This is a sandbox.
Break it, edit the files, delete things. When you want it back the way it
started:

```bash
begin -f demo-plcc-parse
```

That replaces this whole directory with a fresh copy, discarding whatever you
did to it. There is no way to lose anything that matters, because nothing in
here counts.

## What it is for

We worked through this in class. This is the same thing with the tool in front
of you, so you can run it yourself instead of watching me run it.

It is also where **A2** starts. The shape in `spec.plcc` — recursion with an
empty alternative — is the shape A2 question 5 asks you to write, and the class
diagram in section 6 is what A2 questions 1 through 3 are about. Play with it
here first, where being wrong is free.

If you have not done the scanner sandbox yet, do that one first:
`begin demo-plcc-scan`. This one picks up where it stops.

## The files

| File | What it is |
| --- | --- |
| `spec.plcc` | Comma-separated numbers, lexical **and** syntactic. The default. |
| `cap.plcc` | `spec.plcc` with one character changed. Section 2. |
| `empty.plcc` | `spec.plcc`, extended so the empty list is legal too. |
| `ll1.plcc` | The obvious grammar. PLCC refuses it. Section 5. |
| `rep.plcc` | The whole thing in one line. Section 7. |
| `input.txt` | `1, 2, 3` in a file. |

`-s` points `plcc-parse` at a specification other than `spec.plcc`.

> **`-s` is sticky.** Once you pass it, it is remembered for later commands
> until you change it. So after `-s cap.plcc`, a bare `plcc-parse` still uses
> `cap.plcc` — not `spec.plcc`. Pass `-s` explicitly every time below and it
> cannot surprise you.

## 1 — Run it, and read the tree

`spec.plcc` has two sections now, separated by a `%`. The first is a lexical
specification exactly like the ones you wrote in A1. The second is new:

```
<List>          ::= <NUM> <ListTail>
<ListTail:Some> ::= COMMA <NUM> <ListTail>
<ListTail:Zero> ::=
```

Read each rule out loud as a sentence: *"a List is a NUM followed by a
ListTail."* The notation is the only genuinely new thing here, and it stops
being strange once you have said it a few times.

```console
$ echo "1, 2, 3" | plcc-parse -s spec.plcc
List
  NUM '1' [-:1:1]
  Some
    NUM '2' [-:1:4]
    Some
      NUM '3' [-:1:7]
      Zero (empty)
```

`[-:1:1]` is the same **source:line:column** you read off `plcc-scan`.

> **One wrinkle worth knowing.** `plcc-scan` prints the filename when you hand
> it a file. `plcc-parse` prints `-` either way — try `plcc-parse -s spec.plcc
> input.txt` and look. Nothing is wrong; the two tools just disagree, and it
> matters only if you ever try to diff parser output the way A1 step 9 diffed
> scanner output.

## 2 — Where did the commas go?

Look at that tree again. **There is no `COMMA` anywhere in it** — and yet the
grammar says `<ListTail:Some> ::= COMMA <NUM> <ListTail>`, so a comma had to be
there or the parse would have failed.

`cap.plcc` is `spec.plcc` with **one character changed**: `COMMA` became
`<COMMA>`.

```console
$ echo "1, 2, 3" | plcc-parse -s cap.plcc
List
  NUM '1' [-:1:1]
  Some
    COMMA ',' [-:1:2]
    NUM '2' [-:1:4]
    Some
      COMMA ',' [-:1:5]
      NUM '3' [-:1:7]
      Zero (empty)
```

**Angle brackets mean *keep it*. Bare means *require it, then throw it away*.**

You have met this idea before. In A1, `skip` versus `token` was *matched, then
not emitted*. This is *matched, then not kept*. Both times the thing has to be
in the input; both times you choose whether it survives into the next phase.

It is why grammars discard punctuation. Commas, semicolons, parentheses — they
are there to make the notation readable for a human, and they are noise to
whatever runs the program afterward.

## 3 — Recursion, and the rule with nothing on the right

`<ListTail>` mentions `<ListTail>`. That is how a grammar describes a list of
any length without knowing the length in advance.

`<ListTail:Zero> ::=` has **nothing after the `::=`**, and that is legal. It is
the base case — it is the `Zero (empty)` at the bottom of every tree above,
where the list stopped.

One number, one level:

```console
$ echo "1" | plcc-parse -s spec.plcc
List
  NUM '1' [-:1:1]
  Zero (empty)
```

No numbers at all:

```console
$ printf "" | plcc-parse -s spec.plcc
plcc-parser-table: -:1:1: error: unexpected end of file, no production for 'List'
```

`<List> ::= <NUM> <ListTail>` demands at least one number, so the empty list is
not in this language. `empty.plcc` fixes that by splitting `<List>` the same
way `<ListTail>` was split:

```
<List:LSome>    ::= <NUM> <ListTail>
<List:LZero>    ::=
```

```console
$ printf "" | plcc-parse -s empty.plcc
LZero (empty)
```

**The same pattern, applied twice.** That is the technique, not a special case.

## 4 — Judge by the exit status, not by what is printed

```console
$ echo "1," | plcc-parse -s spec.plcc
List
  NUM '1' [-:1:1]
  Some
    COMMA ',' [-:1:2]
plcc-parser-table: -:1:2: error: expected 'NUM', got end of file
```

It printed part of a tree **and then failed**. `plcc-parse` streams the tree as
it goes, so output appearing does not mean the parse succeeded.

Two things to notice in that output, because together they are confusing:

- The parse failed, but you still got tree lines.
- `COMMA ','` shows up **even though `spec.plcc` writes `COMMA` bare**. The
  streaming output prints tokens as it consumes them; the *finished* tree in
  section 1 prints only what was captured. Both are true and they are not in
  conflict.

So test with the exit status:

```console
$ echo "1," | plcc-parse -s spec.plcc >/dev/null && echo PASS || echo FAIL
FAIL
$ echo "1, 2" | plcc-parse -s spec.plcc >/dev/null && echo PASS || echo FAIL
PASS
```

Nothing but `PASS` or `FAIL` — the diagnostics go to stdout, so `>/dev/null`
silences everything. **A2 tells you to test exactly this way.** This is why.

## 5 — A grammar that is right, and still refused

Why write `<ListTail>` at all? Why not just say a list is a number, or a number
and a comma and a list? That is `ll1.plcc`, and it describes the same language:

```
<List:Only> ::= <NUM>
<List:More> ::= <NUM> COMMA <List>
```

```console
$ echo "1, 2, 3" | plcc-parse -s ll1.plcc
plcc-make: error: grammar is not LL(1)

LL(1) conflict: <List> on lookahead NUM

  All of these productions apply:
    <List> ::= <NUM> COMMA <List>
    <List> ::= <NUM>

  This is a FIRST/FIRST conflict: all productions start with NUM, so
  the parser cannot choose between them.

  Tip: left-factor the common prefix:
    <List> ::= <NUM> <ListTail>
    <ListTail> ::= COMMA <List>
    <ListTail> ::=    (empty)
```

**LL(1)** means the parser reads Left to right, builds a Leftmost derivation,
and gets **1** token of lookahead. Standing at `1`, with both rules starting
`<NUM>`, it cannot tell which rule it is in without looking past the number —
and it is not allowed to look.

**Left-factoring** is the fix: pull the shared prefix out, put the difference in
a new non-terminal. That is where `<ListTail>` came from. The grammar in
`spec.plcc` is this one, repaired.

Read that error message closely. When you hit this in A2 — and you will — it
tells you what to do.

## 6 — See the classes your grammar defines

`plcc-diagram` draws pictures of a specification:

```console
$ plcc-diagram -s spec.plcc
plcc-ng/diagram/class.png
plcc-ng/diagram/syntax.png
```

Open `plcc-ng/diagram/class.png`. In Codespaces, click the file in the
Explorer and it opens in a tab.

The class diagram is the useful one here. It shows that your grammar does not
just accept or reject input — **it defines a set of classes**, and the parse
tree is those objects. From `spec.plcc` you get a `List` holding a `Token` and
a `ListTail`; `ListTail` is *abstract*, with `Some` and `Zero` extending it.

Match it against the grammar line by line:

- one class per rule, named by the left-hand side, or by the part after the
  colon when there is one
- one field per **captured** symbol — the `<>` ones from section 2. `Zero` has
  no fields because its rule has no symbols at all.
- field names are the symbol name in camelCase: `<NUM>` becomes `num`,
  `<ListTail>` becomes `listTail`
- several rules with the same left-hand side make the left-hand side abstract
  and each alternative a subclass

**A2 questions 1 through 3 ask you to do this by hand**, from a grammar rule to
a class and its fields. Run `plcc-diagram` on a rule you are unsure about and
check yourself.

> **The syntax diagram is broken for these grammars, and it is not your fault.**
> `syntax.png` comes out saying *Syntax error!* for any grammar with an empty
> alternative — which is `spec.plcc`, `cap.plcc`, and `empty.plcc`. The bug is
> in how PLCC writes the drawing, not in your specification; the class diagram
> beside it is fine, and so is your grammar. It **does** work on `rep.plcc` in
> the next section. Reported upstream.

> `plcc-diagram` renders over the network, so it needs a working connection.
> Everything else in this sandbox runs locally.

## 7 — The same language in one line

`rep.plcc` replaces all three rules with one:

```
<List> **= <NUM> +COMMA
```

`**=` means *repeat*, and `+COMMA` names the separator between repetitions.

```console
$ echo "1, 2, 3" | plcc-parse -s rep.plcc
List
  NUM '1' [-:1:1]
  NUM '2' [-:1:4]
  NUM '3' [-:1:7]
```

**Flat, not nested.** The recursion is gone from the tree — three numbers side
by side under one `List`, which is usually what you wanted anyway. And the
empty list comes free:

```console
$ printf "" | plcc-parse -s rep.plcc
List
```

This one's syntax diagram works, and it is worth looking at — the repetition is
drawn as an actual loop:

```console
$ plcc-diagram -s rep.plcc
```

So why did we do it the hard way first? Two reasons. `**=` is shorthand for
exactly the recursion in section 3, so it is worth knowing what it stands for.
And **A2 question 5 forbids it** — you build the shape by hand once before you
are allowed the shortcut.

## Now break it yourself

No answers below, and nothing to hand in. Predict first, then run.

- In `spec.plcc`, put `<ListTail:Zero>` **above** `<ListTail:Some>`. Does the
  order of alternatives matter the way the order of token rules did in A1?
- Add a `SEMI` token and make the list end with a semicolon. Does the semicolon
  belong in the tree, or not? Write it both ways and look.
- Change `<ListTail:Some>` to `<ListTail:Some> ::= COMMA <List>` — dropping the
  separate `<NUM>`. Does it still parse `1, 2, 3`? Is it still LL(1)?
- Make a grammar for a list of numbers with **no** separator at all, so `1 2 3`
  parses. Then try `**=` with no `+` and compare.
- Write two rules with the same left-hand side that start with the same token,
  on purpose, and read the LL(1) error. Then fix it by left-factoring.
- Run `plcc-diagram` on your own broken grammars. Does the class diagram tell
  you anything the error message did not?

Reset whenever you want with `begin -f demo-plcc-parse`.
