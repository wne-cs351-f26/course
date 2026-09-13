# CS351 - Demo: `plcc-rep`, the semantic section, and meaning

**Nothing here is graded and nothing here is submitted.** This is a sandbox.
Break it, edit the files, delete things. When you want it back the way it
started:

```bash
begin -f demo-plcc-rep
```

That replaces this whole directory with a fresh copy, discarding whatever you
did to it. There is no way to lose anything that matters, because nothing in
here counts.

## What it is for

We worked through this in class. This is the same thing with the tool in front
of you, so you can run it yourself instead of watching me run it.

The parse sandbox ended with a parser that says *yes, `1, 2, 3` is a `List`*.
That is everything the parser knows. This sandbox is about the next question:
**yes — but what does it *mean*?** The answer is a decision you make, written
as Python, in a third section of the same specification. Same grammar, and you
can give it any meaning you like.

If you have not done the parse sandbox yet, do that one first:
`begin demo-plcc-parse`. The grammar here is the one from there.

## Before you run anything — be in the right directory

`begin` put these files in `src/demo-plcc-rep/` inside your repository. Every
command below assumes that is where your terminal is:

```bash
cd src/demo-plcc-rep
```

Same three reasons as the other sandboxes: `-s sum.plcc` is a relative path,
`plcc-ng/` is written into the directory you run from, and the sticky `-s` is
remembered inside it. If a command surprises you, check `pwd` first.

## The files

| File | What it is |
| --- | --- |
| `sum.plcc` | The list grammar plus a semantic section: add the numbers. The textbook's example. |
| `count.plcc` | The **same grammar**, a different meaning: count the numbers. Section 2. |
| `pair.plcc` | Two `<NUM>`s on one right-hand side. PLCC refuses it. Section 5. |
| `pairfix.plcc` | `pair.plcc` with the two numbers told apart. |
| `rep.plcc` | The list with `**=`, and the loop that goes with it. Section 6. |
| `input.txt` | `1, 2, 3` in a file. |

> **`-s` is sticky**, as before. Pass it explicitly every time below and it
> cannot surprise you. **Switching specifications rebuilds `plcc-ng/`**, so
> anything in there — including diagrams — is regenerated from the new one.

## 1 — Run it

`plcc-rep` is *read, eval, print*. It builds the whole interpreter — scanner,
parser, and now your semantic code — and runs it on the input:

```console
$ echo "1, 2, 3" | plcc-rep -s sum.plcc
6
```

Two weeks ago that input produced a list of tokens. Last week, a tree. Today,
**a value**. Open `sum.plcc` and find the third section. Below the second `%`:

- `Python` on its own line — the language the meaning is written in
- a class name on its own line — one for each rule in the grammar
- Python methods between `%%%` and `%%%`, which become methods of that class

The parser is unchanged. Prove it:

```console
$ echo "1, 2, 3" | plcc-parse -s sum.plcc
List
  NUM '1' [-:1:1]
  Some
    NUM '2' [-:1:4]
    Some
      NUM '3' [-:1:7]
      Zero (empty)
```

Same tree as the parse sandbox. `plcc-rep` is that tree, *plus* your code.

## 2 — Same grammar, different meaning

`count.plcc` has the **identical** lexical and syntactic sections. Only the
Python differs:

```console
$ diff sum.plcc count.plcc
16c16
< # Compute the sum of the numbers
---
> # Count the numbers
23,25c23,24
<     n = int(self.num.lexeme)
<     sum = n + self.listTail.eval()
<     return str(sum)
---
>     count = 1 + self.listTail.eval()
>     return str(count)
31,33c30
<     n = int(self.num.lexeme)
<     sum = n + self.listTail.eval()
<     return sum
---
>     return 1 + self.listTail.eval()
```

```console
$ echo "1, 2, 3" | plcc-rep -s count.plcc
3
```

**Same input. Same tokens. Same tree. Different answer.** Nothing about
whether `1, 2, 3` is a legal program changed — that is *syntax*, and the
grammar settles it. What the program *does* is *semantics*, and the grammar
has nothing to say about it. That is the distinction the whole course is
built on, and this is what it looks like in two files.

Make a third. Copy `sum.plcc` to `product.plcc` and change as little as you
can so that `1, 2, 3` gives `6` for a different reason, and `2, 3, 4` gives
`24`. Think about what `Zero` has to return now.

## 3 — The classes are real, and your code goes inside them

The parse sandbox said a grammar *defines classes*. Look at them:

```console
$ plcc-diagram -s sum.plcc
plcc-ng/diagram/class.png
plcc-ng/diagram/syntax.png
```

Open `plcc-ng/diagram/class.png` (in Codespaces, click it in the Explorer).
`List` has fields `num` and `listTail`. `ListTail` is abstract; `Some` and
`Zero` extend it. `Zero` has no fields.

Now look at the actual Python PLCC generated:

```console
$ cat plcc-ng/Python/List.py
```

```python
class List(_Start):

    _rule_name = "List"
    _fields = ["num", "listTail"]

    def __init__(self, num, listTail):
        super().__init__()
        self.num = num
        self.listTail = listTail

    def _run(self):
        n = int(self.num.lexeme)
        sum = n + self.listTail.eval()
        return str(sum)
```

That `_run` is yours, copied out of `sum.plcc` and pasted into a class PLCC
wrote. So `self.num` and `self.listTail` are not magic names — they are the
fields from the diagram, and the diagram is the grammar rule:

| In the rule | In the class | Type |
| --- | --- | --- |
| `<NUM>` | `self.num` | `Token` — has a `.lexeme`, which is a **string** |
| `<ListTail>` | `self.listTail` | whichever subclass the parser built, `Some` or `Zero` |
| `COMMA` | *nothing* | not captured, so not a field |

**The naming rule:** a token's name in lowercase (`<NUM>` → `num`); a
non-terminal's name with its first letter lowered (`<ListTail>` → `listTail`).
If you are ever unsure what a field is called, this file is the answer.

> **If `syntax.png` says *Syntax error!*, it is not your fault.** Same PLCC
> drawing bug as the parse sandbox, triggered by the empty alternative. The
> class diagram is correct and so is your specification.

> `plcc-diagram` renders over the network. Everything else here runs locally.

## 4 — Where `6` comes from

Put the tree from section 1 next to the code and follow it:

1. `plcc-rep` calls `_run` on the **root** — `List`. That is the rule for the
   start symbol: it must define `_run`, and `_run` must return a **string**.
2. `List._run` turns its own `'1'` into `1`, then asks its tail: `self.listTail.eval()`.
3. That tail is a `Some` holding `'2'`, which asks *its* tail.
4. Which is a `Some` holding `'3'`, which asks *its* tail.
5. Which is `Zero`. `Zero.eval` returns `0`. **This is where the recursion
   stops** — the empty alternative in the grammar is the base case in the code.
6. `3 + 0`, then `2 + 3`, then `1 + 5`. `_run` returns `'6'`.

Two things to notice, because both will bite you later:

**The lexeme is a string.** `self.num.lexeme` is `'1'`, not `1`. It is `int(...)`
that makes it a number — *you* decide what the characters mean, the scanner
does not. If your language had octal numbers you would write
`int(self.num.lexeme, base=8)`; for decimals, `float(...)`.

**`_run` returns a string.** `str(sum)` is not decoration. Delete it and run:

```console
$ echo "1, 2, 3" | plcc-rep -s sum.plcc
Specification error: TypeError: _run() must return a string, got int
Fix the errors in your specification and re-run.
```

The other methods — `eval` here — are yours to name and can return anything;
only `_run` on the start symbol has rules.

## 5 — Two of the same symbol

`pair.plcc` describes a pair of numbers:

```
<Pair> ::= <NUM> COMMA <NUM>
```

```console
$ echo "4, 5" | plcc-rep -s pair.plcc
plcc-make: plcc-validate-syntactic failed (exit 1)
plcc-validate-syntactic: pair.plcc:8:1: error: duplicate RHS symbol name 'num' — all capturing RHS symbols must have unique names
<Pair> ::= <NUM> COMMA <NUM>

^
```

Both `<NUM>`s would become a field called `num`, and the semantic code could
not tell them apart. PLCC refuses rather than guess. `pairfix.plcc` adds a
suffix to each:

```
<Pair> ::= <NUM:m> COMMA <NUM:n>
```

and the fields are now `self.m` and `self.n`:

```console
$ echo "4, 5" | plcc-rep -s pairfix.plcc
A pair containing 4 and 5
```

You met the same `:suffix` last week on the *left* side, naming alternatives
(`<ListTail:Some>`). On the right side it names fields. Same notation, same
idea: **a suffix is how you tell two things with the same name apart.**

## 6 — `**=` and the list it gives you

`rep.plcc` writes the grammar in one line, as the parse sandbox did:

```
<List> **= <NUM> +COMMA
```

One rule means one class, and instead of a chain of `Some`s there is one field
holding **a Python list** of tokens. Its name is the symbol's name plus `List`:
`<NUM>` → `numList`.

```python
def _run(self):
    sum = 0
    for n in self.numList:
        sum += int(n.lexeme)
    return str(sum)
```

```console
$ echo "1, 2, 3" | plcc-rep -s rep.plcc
6
$ printf "" | plcc-rep -s rep.plcc
0
```

No recursion, no base case, and the empty list is free. Two grammars for the
same language; the shape of the grammar is the shape of the code you write for
it.

## Now break it yourself

No answers below, and nothing to hand in. Predict first, then run.

- **Product**, if you did not do it in section 2. Then **largest number**. What
  does `Zero` return for each? Is there a right answer for the largest of an
  empty list?
- **Average**, as a decimal: `1, 2, 4` gives `2.3333…`. You will need `float`,
  and you will need to know the count *and* the sum. Can one `eval` return both?
- Delete `str(` … `)` from `_run` and read the error. Now put it back and make
  `Zero.eval` return `'0'` — a string — instead of `0`. What breaks, and where?
- Rename `Zero`'s method from `eval` to `evaluate`, leaving the others alone.
  Read the error. Who is calling `eval`, and on what?
- Rename `_run` to `run`. It builds and runs — and prints
  `<List.List object at 0x…>`. Why is nothing complaining?
- Delete the line that says `Python`. The error is not about `Python`. Work out
  why it says what it says.
- In `sum.plcc`, change `<ListTail:Some> ::= COMMA <NUM> <ListTail>` to
  `COMMA NUM <ListTail>` — capture removed. The grammar is still fine. Run
  `plcc-rep` and see which side complains, the syntax or the semantics.
- Give `pairfix.plcc` two pairs on two lines and see what `plcc-rep` does.
  Then give `sum.plcc` two lists on two lines. One of them works. Why?

Reset whenever you want with `begin -f demo-plcc-rep`.
