# CS351 - Demo: `V0`, the first language

**Nothing here is graded and nothing here is submitted.** This is a sandbox.
Break it, edit the files, delete things. When you want it back the way it
started:

```bash
begin -f demo-v0
```

That replaces this whole directory with a fresh copy, discarding whatever you
did to it. There is no way to lose anything that matters, because nothing in
here counts.

## What it is for

We worked through this in class. This is the same thing with the tool in front
of you, so you can run it yourself instead of watching me run it.

The three sandboxes before this one built up a specification one section at a
time, on a language that was only ever a list of numbers. `V0` is the first
*real* language of the course: arithmetic expressions, nested as deep as you
like, with variables. Its meaning is nothing more than to print the program
back. Every language after it is `V0` plus one idea, so the point of this
sandbox is to be able to read `V0` whole — all three sections, and the classes
they turn into — before anything gets added.

If you have not done the earlier sandboxes, do `demo-plcc-rep` first. Every
rule here is one you met there, applied to a bigger grammar.

## Before you run anything — be in the right directory

`begin` put these files in `src/demo-v0/` inside your repository. Every
command below assumes that is where your terminal is:

```bash
cd src/demo-v0
```

Same three reasons as before: `-s v0.plcc` is a relative path, `plcc-ng/` is
written into the directory you run from, and the sticky `-s` is remembered
inside it. If a command surprises you, check `pwd` first.

## The files

| File | What it is |
| --- | --- |
| `v0.plcc` | `V0`, complete: the textbook's lexical and syntactic sections plus the semantic section it points at. |
| `input.txt` | A `V0` program with some whitespace and a comment in it. |
| `scheme.plcc` | `v0.plcc` with **two lines** changed in the semantic section. Section 6. |
| `mul.plcc` | `v0.plcc` plus one operator, `*` — one line in each section. Section 5, finished. |
| `order.plcc` | `v0.plcc` with **one token line moved**. Section 7. |

> **`-s` is sticky**, as before. Pass it explicitly every time below and it
> cannot surprise you. **Switching specifications rebuilds `plcc-ng/`.**

## 1 — Run it

```console
$ cat input.txt
add1(   +(2, 3))  % a comment
$ plcc-rep -s v0.plcc input.txt
add1(+(2,3))
```

The spaces are gone and so is the comment. Nothing in the semantic section
deletes them — they never got that far. Look at the first section of
`v0.plcc`: two `skip` lines. The scanner matched them and did not emit them,
exactly as it did with whitespace in the first sandbox. Prove it:

```console
$ plcc-scan -s v0.plcc input.txt
input.txt:1:1 ADD1OP 'add1'
input.txt:1:5 LPAREN '('
input.txt:1:9 ADDOP '+'
input.txt:1:10 LPAREN '('
input.txt:1:11 LIT '2'
input.txt:1:12 COMMA ','
input.txt:1:14 LIT '3'
input.txt:1:15 RPAREN ')'
input.txt:1:16 RPAREN ')'
```

Nine tokens, no comment, no spaces. What `plcc-rep` printed is not the input
cleaned up; it is the **tree**, printed out again in a fixed format. The
textbook calls this a pretty-printer. Notice the output has commas and
parentheses in it even though the grammar throws both away (they are bare
symbols). Who put them back? Keep that question for section 4.

## 2 — Three kinds of expression

Open `v0.plcc` at the second section. Nine rules. Then draw the classes:

```console
$ plcc-diagram -s v0.plcc
plcc-ng/diagram/class.png
plcc-ng/diagram/syntax.png
```

Open `plcc-ng/diagram/class.png` and put it beside the grammar. Go rule by
rule, and for each one say the class *before* you look at the picture — the
rules you learned in `demo-plcc-rep` are all you need:

| Rule | Class | Why |
| --- | --- | --- |
| `<Program> ::= <Exp>` | `Program { exp: Exp }` | one class per rule, one attribute per captured symbol |
| `<Exp:LitExp> ::= <LIT>` | `Exp` **abstract**; `LitExp { lit: Token }` | shared left-hand side → abstract parent, one subclass per alternative |
| `<Exp:VarExp> ::= <SYMBOL>` | `VarExp { symbol: Token }` | same shape, different token |
| `<Exp:PrimappExp> ::= <Prim> LPAREN <Rands> RPAREN` | `PrimappExp { prim: Prim, rands: Rands }` | the parentheses are **bare** — required, then thrown away |
| `<Rands> **= <Exp> +COMMA` | `Rands { expList: list of Exp }` | one rule, one list, as in `rep.plcc` — the picture writes it `expList: Exp`, naming the *element* type |
| `<Prim:AddPrim> ::= ADDOP` | `Prim` **abstract**; `AddPrim { }` | **no attributes at all** |

(The textbook and the diagram say *attribute*; the generated code says
`_fields`; the earlier sandboxes said *field*. Same thing.)

That last row is the new thing. Four `Prim` classes, and none of them holds
anything. Ask the question from the parse sandbox: *how many lexemes could
`ADDOP` match?* Exactly one — `+`. There is nothing to keep, because the name
of the token already tells you everything. So the token is bare, the class is
empty, and **the class name is the information**. That is why the tree prints
it the way it does:

```console
$ echo '+(3, x)' | plcc-parse -s v0.plcc
Program
  PrimappExp
    AddPrim (empty)
    Rands
      LitExp
        LIT '3' [-:1:3]
      VarExp
        SYMBOL 'x' [-:1:6]
```

`AddPrim (empty)` is not a missing `+`. It is the `+`. The parser recorded
*which* `Prim` it built, and that is the whole fact.

Compare `LIT`: it could match `3`, `42`, `2026`. You would still have a
question after matching it, so it is captured, and `LitExp` has a `lit`.

## 3 — Nesting

```console
$ echo '+(3, add1(x))' | plcc-parse -s v0.plcc
Program
  PrimappExp
    AddPrim (empty)
    Rands
      LitExp
        LIT '3' [-:1:3]
      PrimappExp
        Add1Prim (empty)
        Rands
          VarExp
            SYMBOL 'x' [-:1:11]
```

A `PrimappExp` inside the `Rands` of another `PrimappExp`. The list grammar
recursed through one rule mentioning itself; `V0` recurses through a **cycle**:
`Exp` → `PrimappExp` → `Rands` → `Exp`. No rule names itself, and the language
still nests without limit. Each pair of parentheses in the input is one more
`PrimappExp` in the tree — depth of the parentheses is depth of the tree.

`Rands` is a `**=` rule, so its operands are **siblings** in a list, not a
chain of `Some`s. Two operands, two children. Compare the shape to the
recursive list in `demo-plcc-rep` if you want to see the difference again.

## 4 — `__str__`: one method, every class

Now the third section. `Program` is the start symbol, so it has `_run`, and
`_run` is one line:

```python
def _run(self):
    return str(self.exp)
```

Every other class defines `__str__` — eight of them. And **nothing ever calls
`__str__` by name.** Look at what does:

- `str(self.exp)` in `_run` — Python calls `self.exp.__str__()` for you.
- `f"{self.prim}({self.rands})"` in `PrimappExp` — an f-string calls
  `__str__` on each thing it inserts. *This* is who puts the parentheses back.
- `",".join(str(e) for e in self.expList)` in `Rands` — `str(e)` on every
  operand, and the commas come from `join`.
- `return self.lit.lexeme` in `LitExp` — the bottom. A string, no further calls.

`__str__` is a *dunder* (double underscore) method: Python's name for
"how do you print yourself?" You are not defining a method PLCC knows about;
you are answering a question Python asks. The same goes for `__init__`, which
PLCC wrote for you.

The thing to see is the **shape**. `PrimappExp.__str__` calls `str(self.prim)`
without knowing — or caring — which of the four `Prim`s it holds. Each `Prim`
answers for itself. Every class in the tree implements the *same* method, each
in its own way, and the tree prints itself by each node asking its children.
**That is how every language after this one works too**: one method name,
one implementation per alternative, and a walk from the root down.

Read `plcc-ng/Python/PrimappExp.py` and `AddPrim.py` if you want to see the
methods sitting inside the classes PLCC wrote; `_fields = []` in `AddPrim` is
section 2 again.

## 5 — Add an operator

`V0` has no multiplication. Add it. Work in a copy, so `v0.plcc` stays as it
was for the sections after this one:

```console
$ cp v0.plcc mymul.plcc
$ echo '*(2, 3)' | plcc-rep -s mymul.plcc
plcc-tokens: -:1:1: error: unrecognized character '*'
```

The **scanner** has never seen `*`. Add `token MULOP '\*'` to the first
section of `mymul.plcc`, right after `SUBOP`, and run it again:

```console
$ echo '*(2, 3)' | plcc-rep -s mymul.plcc
plcc-parser-table: -:1:1: error: unexpected 'MULOP', no production for 'Program'
```

The scanner is happy; the **parser** has a token no rule mentions. Add
`<Prim:MulPrim> ::= MULOP` to the second section, right after `SubPrim`:

```console
$ echo '*(2, 3)' | plcc-rep -s mymul.plcc
<MulPrim.MulPrim object at 0x7f8abe5f46e0>(2,3)
```

(The number after `at` is a memory address; yours will differ.)

Parsed, built, printed — and `MulPrim` printed itself the way Python prints
any object with no `__str__` of its own. Not an error, which is worth
remembering: a missing method here is *silent*. Add `MulPrim` with a
`__str__` returning `"*"` to the third section:

```console
$ echo '*(2, 3)' | plcc-rep -s mymul.plcc
*(2,3)
```

`mul.plcc` is the finished version; `diff mymul.plcc mul.plcc` should show
no difference except the comment at the top and, if you put `MulPrim`
somewhere else in the third section, the order of the classes — which does
not matter.

Three sections, three failures — two errors and one silent wrong answer —
each from a different phase, each telling you which section you had not
written yet. This is what "`V0` plus one idea"
costs, and every language from here on is built by exactly this kind of
addition.

## 6 — Same grammar, different meaning

`scheme.plcc` changes two lines in the semantic section — `PrimappExp.__str__`
and `Rands.__str__` — and nothing else:

```console
$ diff v0.plcc scheme.plcc
1,3c1,2
< # Language V0: the lexical and syntactic sections from the textbook chapter,
< # plus the semantic section the chapter points at. Its meaning is to print
< # the program back.
---
> # V0 with two lines changed in the semantic section: it prints the program
> # back as a Scheme expression. Same tokens, same grammar, same tree.
38c37
<     return f"{self.prim}({self.rands})"
---
>     return f"({self.prim} {self.rands})"
44c43
<     return ",".join(str(e) for e in self.expList)
---
>     return " ".join(str(e) for e in self.expList)
$ echo 'add1(+(3, -(x, 2)))' | plcc-rep -s scheme.plcc
(add1 (+ 3 (- x 2)))
```

The first hunk is the comment at the top of each file. The other two are the
whole change.

That is the same program in Scheme. Same tokens, same tree, same classes, and
a different language coming out, because the grammar says what a `V0` program
*is* and only the third section says what it *means*. The textbook's
Discussion section talks about prefix notation and the Lisp family; this is
that paragraph, runnable.

## 7 — The tie-break, again

Look at the lexical section once more. `add1` matches both `ADD1OP` and
`SYMBOL`, at the same length. Which wins?

```console
$ echo 'add1(add1x, x1)' | plcc-scan -s v0.plcc
-:1:1 ADD1OP 'add1'
-:1:5 LPAREN '('
-:1:6 SYMBOL 'add1x'
-:1:11 COMMA ','
-:1:13 SYMBOL 'x1'
-:1:15 RPAREN ')'
```

`add1` is `ADD1OP` because that line comes first; `add1x` is a `SYMBOL` because
longest match beats rule order. `order.plcc` moves the `SYMBOL` line above the
operators. Same tokens, same grammar, same semantics, one line in a different
place:

```console
$ echo 'add1(2)' | plcc-rep -s order.plcc
add1
plcc-parser-table: -:1:5: error: unexpected 'LPAREN', no production for 'Program'
```

Two things to explain. The error comes from the **parser**, but the mistake is
in the **lexical** section: `add1` scanned as a `SYMBOL`, so the parser —
correctly — built a `VarExp` and was done. The parser is not wrong; it was
handed the wrong tokens. When an error names a phase, the mistake can still be
in an earlier one.

And why did `add1` print at all? Because `plcc-rep` does not read *one*
program — it reads programs until the input runs out, and a `V0` program has
no terminator. `add1` was a complete `VarExp`, so it ran and printed. Then
`plcc-rep` started reading a second program at `(`, and no `Exp` starts with
`LPAREN`. You can see the same thing with two good programs:

```console
$ printf '3\nx\n' | plcc-rep -s v0.plcc
3
x
```

So when `plcc-rep` prints something and *then* fails, read it as two programs:
one that worked, and one that did not.

## Now break it yourself

No answers below, and nothing to hand in. Predict first, then run.

- Add `*` yourself, from `v0.plcc`, without looking at `mul.plcc`. Then add
  a two-character operator, `**`. What decides whether `**` scans as one
  token or two `*`s?
- Write `scheme.plcc` yourself from `v0.plcc` if you only read section 6.
  Then, in `v0.plcc`, make `Rands` join with `", "` instead of `","` — now
  it is *pretty*.
- Delete `LitExp`'s `__str__` and run `+(3, x)`. Then delete `AddPrim`'s
  instead. Read what prints. Why is there no error?
- Put a `%` comment in the middle of an expression, and put the rest of the
  expression on the next line. Does it still parse? Which `skip` line is
  responsible for each half of the answer?
- `+()` — run it. Is that a `V0` program? What in the grammar says so?
- Run `ADD1(2)`. Predict the tokens first.
- Move `token LIT '\d+'` to the bottom of the lexical section. Does anything
  change? Why did moving `SYMBOL` matter in section 7 and moving `LIT` not?
- In `v0.plcc`, change `<Rands> **= <Exp> +COMMA` to `<Rands> **= <Exp>` and
  run `+(3, x)`, then `+(3 x)`. What did the comma do for the parser, and
  what does the pretty-printer do about it now?
- `plcc-diagram -s scheme.plcc` and compare `class.png` to the one from
  section 2. Explain the result in one sentence.

Reset whenever you want with `begin -f demo-v0`.
