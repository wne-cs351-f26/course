# CS351 - Assignment a2

## Purpose

A1 was about the first phase: turning characters into tokens. This assignment
is the other two — turning tokens into **structure**, and giving that structure
**meaning** — and it ends with the first real language of the course, `V0`,
which every later language is built by extending.

The idea underneath both phases is the one A1 started: a language is something
you *specify*. A grammar specifies which token sequences are programs, and the
parser PLCC generates from it says *yes* or *no* — and when it says yes, it
hands you a tree. But *yes* is all it says. What a program **does** is a
separate decision, written as Python methods on classes that PLCC generates
*from the grammar*.

You are not being asked to design languages yet. From here on we will define a
series of small languages together, syntax and semantics for each construct,
and your job in this assignment is to be ready to **read** them: given a
specification, predict what the scanner, the parser, and the interpreter will
do with an input — and when one of them reports an error, say what is probably
wrong and where in the specification to look.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[Syntax](https://ourplcc.github.io/course-materials-ng/dev/04-syntax/),
[Semantic](https://ourplcc.github.io/course-materials-ng/dev/05-semantic/), and
[V0](https://ourplcc.github.io/course-materials-ng/dev/06-v0/).

**The three sandboxes** we used in class, `demo-plcc-parse`, `demo-plcc-rep`,
and `demo-v0`, are the same material with the tool in front of you. Work
through them before starting. Every question below assumes you have.

### What you will be able to do

1. **Place the three phases.** Say what each of scanning, parsing, and
   semantic analysis takes in and hands on, and, given an error message, say
   which phase produced it.

2. **Predict what the parser does.** Given a grammar and an input, say whether
   the input parses and draw the tree it produces. Given a rejected input,
   say where the parse stopped and what it expected.

3. **Read a grammar rule as a class.** For any rule, name the class it
   defines, say whether it is abstract or a subclass, and list its attributes
   with their names and types — then check yourself against the code PLCC
   generates.

4. **Predict what the interpreter does.** Given a specification with a
   semantic section and an input, trace the methods that run, in order, and
   say what is printed. Say what changes in the output, and what does not,
   when only the semantic section is changed.

5. **Diagnose a specification that does not build or does not run.** From
   the error, say what kind of mistake it is — a grammar PLCC refuses, a
   missing or misnamed attribute, a method that is not there or returns the
   wrong kind of thing — and which section to look in.

6. **Read `V0`.** Say what a `V0` program means, which rule each part of it
   matched, and how its semantics walks the tree to print it back.

### The core concepts

These are what the Correctness criterion looks at. Details — a tree drawn
with slightly different indentation, a class named from memory instead of
from the diagram — are worth a comment from me but cost you nothing. These
are what matter:

- **Syntax versus semantics, made concrete.** The parser decides whether
  `1, 2, 3` is a program; it does not decide what the program does. The same
  grammar can carry any meaning. A student who has this can say what changes
  and what does not when only the semantic section changes.

- **Terminal, non-terminal, rule, start symbol.** A terminal is a token from
  the lexical section; a non-terminal is defined by rules; the start symbol is
  the left-hand side of the first rule, and the root of every tree.

- **Capture.** `<X>` keeps the symbol as an attribute; bare `X` requires it and
  throws it away. That is why the commas are not in the tree.

- **Recursion and the empty alternative.** A rule that mentions itself
  describes any length; the alternative with nothing on the right is where it
  stops — in the tree, and in the code that walks it.

- **Grammar → class → attributes.** One class per rule, named for the
  left-hand side or its suffix; a left-hand side with several rules is
  abstract, one subclass per alternative. One attribute per captured symbol:
  a token gives a `Token` whose `.lexeme` is a **string**; a non-terminal
  gives an instance of its class; a `**=` symbol gives a Python list named
  `xList`. This is what makes `self.num` and `self.listTail` readable.

- **What a syntax error is.** Not "the parser got confused" — the specific
  situation where the next token fits no rule, and the parser telling you
  where, what it expected, and what it got. A tree printed above the error
  does not mean it parsed: read to the end.

- **A grammar can be right and still be refused.** *Describes the language*
  and *parseable by this method* are different properties. When PLCC reports
  an LL(1) conflict, the error names the rules involved and offers a fix.

### Where this leads

A3 makes the tree *evaluate* itself. `V0` only prints its input back; the next
languages compute with it, and to do that they need **environments** — the
machinery for what a name means at a given point in a program. That is the
subject of the two weeks after this assignment goes out, and every `V` after
`V0` is `V0` plus one idea. Writing grammars and semantics of your own comes
later, once you have read several.

On Exam 1, this material shows up as things you can only do by having run
them: draw the tree a grammar produces for an input, name the class and
attributes a rule defines, trace what an interpreter prints, and say what a
given error means and where you would look.

## How to do this assignment

**Your answers go in this file.** Every question has one or more `ANSWER`
blocks that look like this:

````
```
Replace this line with your answer.
```
````

Replace that line with your answer and leave the fences around it alone.

Most questions ask you to **predict first, then run.** Write the prediction
down before you run anything, then run it, then say whether you were right.
The prediction is where the learning is; the run is only the check. A wrong
prediction followed by an honest correction is a complete answer — and it is
the kind of answer that tells me something worth responding to.

Every question has its own directory, `q1/` through `q5/`, with the files it
uses. Position your terminal in that directory before running anything in it —
`-s` takes a relative path, and the build cache `plcc-ng/` is written wherever
you run from. The only file you edit that is graded is `q3/sum.plcc`.

How this is scored is the same as A1: [GRADING.md](../../GRADING.md), three
criteria, nine points. The **core concepts** listed above are what Correctness
looks at.

When you are done, run `save` from anywhere in your repository. **Your work is
not submitted until `save` has run.** It is safe to run as often as you like.


## QUESTION 1 — A rule is a class

`q1/spec.plcc` is a complete specification for a language that means nothing.
Its semantic section is empty on purpose: PLCC still generates a Python class
for every rule, and those classes are what this question is about. Three of
the rules are marked `(a)`, `(b)`, and `(c)`:

```
<Blah:Goo>     ::= THIS <VAR> IS <Silly>                                   # (a)
<Many>         **= EACH <Rule> HAS MULTIPLE OCCURRENCES <OF> <Stuff>       # (b)
<Classes>      ::= ME AM TAKING <CSIT:c1> <CSIT:c2> AND <CSIT:c3>          # (c)
```

For each of the three, **before running anything**, write the class PLCC
will generate, as Python — the `class` line and the `__init__`, in the shape
you saw in `List.py` in the `demo-plcc-rep` sandbox — and put the **type** of
each attribute in a comment beside it, since Python will not say. For the
sandbox's `<ListTail:Some> ::= COMMA <NUM> <ListTail>` that would be:

```python
class Some(ListTail):
    def __init__(self, num, listTail):
        self.num = num              # Token
        self.listTail = listTail    # ListTail
```

A type is `Token`, the name of a class, or a list of either — write those as
`list of Token` or `list of Silly`. Bare symbols get no attribute. If a rule
also implies a class that is *not* the one it names — a parent, say — write
that class too.

### ANSWER — (a)

```
Replace this line with your answer.
```

### ANSWER — (b)

```
Replace this line with your answer.
```

### ANSWER — (c)

```
Replace this line with your answer.
```

Now check yourself. Run the specification once so PLCC generates its classes,
then read them:

```bash
cd q1
plcc-rep -s spec.plcc input
cat plcc-ng/Python/Goo.py plcc-ng/Python/Many.py plcc-ng/Python/Classes.py
```

The line `plcc-rep` prints is a Python object with no `_run` to give it a
meaning — expected, since the semantic section is empty. The files are what
you want. Two things in them you can ignore: the `import` lines, and
`(_plcc.Node)` on a class with no parent of its own — that is PLCC's base
class for every node.

The generated code checks your **names** and **parents**. It cannot check
your **types**, because Python does not write them down. For those, run
`plcc-diagram -s spec.plcc` and open `plcc-ng/diagram/class.png`: it labels
every attribute with a type. One thing to know when reading it: for a
`**=` rule it names the type of each *element* — `ruleList: Rule` — rather
than saying *list of*.

**(d)** Report every place the generated code disagrees with what you wrote,
and for each one say which of you was right and why. If it agrees with you
everywhere, say so.

Then one more, which the generated code shows but the rule does not say out
loud: `Blah` has only one rule, yet `Blah.py` exists as its own class with
`Goo` extending it. **What in the way the rule is written makes that happen?**

### ANSWER — (d)

```
Replace this line with your answer.
```


## QUESTION 2 — Predict the parser

`q2/spec.plcc` describes strings of balanced parentheses ending in an at-sign:

```
<Start>          ::= <Balanced> AT
<Balanced:Pair>  ::= LPAREN <Balanced:inside> RPAREN <Balanced:after>
<Balanced:Empty> ::=
```

`q2/` also holds five one-line input files, `legal-1`, `legal-2`, and
`illegal-1` to `illegal-3`. **Do not run anything until part (a) is written.**

**(a)** For each of the five files, read the input and the grammar and
predict: does it parse? One line per file. Then run each one —

```bash
cd q2
plcc-parse -s spec.plcc legal-1
```

— and mark each prediction right or wrong. A tree is printed even when the
parse fails, so read to the **last line** of the output before deciding.

### ANSWER

```
Replace this line with your answer.
```

**(b)** `legal-2` is `(())()@`. Draw the parse tree by hand, in the same
indented form `plcc-parse` uses. Every `Pair` node has two `Balanced`
children; **label each one `inside` or `after`** — `plcc-parse` does not, and
telling them apart is the point. Then run it and compare.

### ANSWER

```
Replace this line with your answer.
```

**(c)** `illegal-1` is `())@` and `illegal-2` is `(@`. For each, before
running: at which character does the parse stop, what does the parser
*expect* there, and what does it *get*? Then run and check against the error
line.

### ANSWER

```
Replace this line with your answer.
```

**(d)** Every successful tree in (a) contains only `Start`, `Pair`, and `Empty`
nodes. The input was full of parentheses. **Where did they go, and what in
the grammar sent them there?** Then: which symbol is the grammar's start
symbol, and how do you know?

### ANSWER

```
Replace this line with your answer.
```

**(e)** `illegal-3` is `()` — no at-sign. The error it produces does **not**
say `expected 'AT'`. Read the message, then explain from the grammar: after
the `)`, what was the parser trying to build when it ran out of input, and
what would the input have needed next for that to succeed?

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 3 — Predict the interpreter, then finish one

`q3/min.plcc` is a complete specification: LONN, a non-empty list of natural
numbers in parentheses, whose meaning is the **smallest** number in the list.
Read all three sections before starting.

**(a)** `input-1` is `(3 5 2 4)`. Before running, predict what `plcc-rep`
prints. Then list **every method call**, in the order it happens, with the
value of its argument, in this form:

```
Lonn._run()
More.min(3)
...
```

Then run it:

```bash
cd q3
plcc-rep -s min.plcc input-1
```

### ANSWER

```
Replace this line with your answer.
```

**(b)** `input-3` is `()`. Predict what happens, then run it. **Which of the
three phases** produced the message, and **which line of the specification**
is the reason `()` is not a LONN program?

### ANSWER

```
Replace this line with your answer.
```

**(c)** In `min.plcc`, change the `<` in `More.min` to `>`. Nothing else.
Predict what `input-1` prints now, then run it. Then run `plcc-parse -s
min.plcc input-1` and compare its tree to the one you get from the original
file. **What changed, and what did not?** Use the words *syntax* and
*semantics* in your answer. (`min.plcc` is not graded; leave it either way.)

### ANSWER

```
Replace this line with your answer.
```

**(d)** `q3/sum.plcc` is the same language with a different meaning: the
**sum** of the numbers. The grammar, `Lonn._run`, and `Done.sum` are written.
`More.sum` is a stub.

First run it as it stands on `sum-input` and explain the output — what did the
stub return, and how did that become what was printed?

Then write the body of `More.sum`. It is one or two lines, and `More.min` is
the model. `sum-input` holds three programs and `sum-expected` holds the three
answers, so:

```bash
plcc-rep -s sum.plcc sum-input | diff - sum-expected
```

prints nothing when you are done. Paste your finished `More.sum` here as well
as leaving it in the file.

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 4 — Something is wrong

`q4/` holds five specifications, `broken-1.plcc` to `broken-5.plcc`. Each is
`q3/min.plcc` with one mistake introduced. `q4/input` is `(3 5 2 4)`.

For each one, run it —

```bash
cd q4
plcc-rep -s broken-1.plcc input
```

— and answer three things:

1. **Which phase complained?** Scanning, parsing, or the semantics — or
   PLCC refusing to build the specification at all. Say what in the message
   tells you.
2. **What is wrong**, in one sentence.
3. **The fix**: the corrected line — or, if the mistake is something that
   should not be there at all, say what to delete. Make the change and run it
   again — the fix is right when the output is `2`, the same as
   `q3/min.plcc`. A change that silences the error but prints something else
   is a different mistake.

One of the five is refused with a long message that ends in a *Tip*. The tip
is a correct fix. It is not the *smallest* one — the question is what was
added to `min.plcc`, and the smallest fix takes it back out.

### ANSWER — broken-1

```
Replace this line with your answer.
```

### ANSWER — broken-2

```
Replace this line with your answer.
```

### ANSWER — broken-3

```
Replace this line with your answer.
```

### ANSWER — broken-4

```
Replace this line with your answer.
```

### ANSWER — broken-5

```
Replace this line with your answer.
```


## QUESTION 5 — Read V0

`q5/spec.plcc` is `V0`, complete: the lexical and syntactic sections from the
textbook chapter, plus the semantic section the chapter points at. Read all
three before starting. Its meaning is to print the program back.

**(a)** For each of these, predict: is it a `V0` program? If yes, which
alternative of `<Exp>` matches the *whole* thing? If no, where does it fail?
Then run each through `plcc-parse` and check.

```
x
+(4, -(5, 2))
sub1(x, 3)
+(1 2)
3 + 4
```

There is no input file for these; type them in, or `echo` them:

```bash
cd q5
echo '+(4, -(5, 2))' | plcc-parse -s spec.plcc
```

### ANSWER

```
Replace this line with your answer.
```

**(b)** `V0` spends four token lines and five grammar rules on its operators.
Here is another way to write the same language. Copy `spec.plcc` to
`oneprim.plcc` and make exactly these changes: replace the four operator
tokens with one, in the same place,

```
token PRIMOP '\+|-|add1|sub1'
```

change `PrimappExp` to capture it directly,

```
<Exp:PrimappExp> ::= <PRIMOP> LPAREN <Rands> RPAREN
```

and delete the four `<Prim:…>` rules. Leave the semantic section alone.

Then answer these four, in order:

1. **Before running anything**, predict the `plcc-parse` tree for
   `+(4, -(5, 2))` under `oneprim.plcc`. Say what appears where
   `AddPrim (empty)` was, and explain from the two grammars why one design
   prints `(empty)` there and the other does not. Then run it and check.

2. Run `plcc-rep -s oneprim.plcc` on the same input. It fails. Say which
   attribute of which class it is looking for and why that attribute is no
   longer there.

3. Give the one-line change to `PrimappExp.__str__` that makes it print
   `+(4,-(5,2))` again. Make the change and confirm.

4. The question the exercise is for. Both specifications accept exactly the
   same programs and print exactly the same output. In each, *where* is the
   fact that this operator is `+` and not `-` — what holds it, and what kind
   of thing is it? Now suppose each operator had to do something different —
   actually add, actually subtract. In the original `V0`, which class would
   the code for `+` go in? In `oneprim.plcc`, where would it have to go, and
   what would that code look like?

### ANSWER

```
Replace this line with your answer.
```

**(c)** The semantic section defines `_run` once and `__str__` eight times,
and no method ever calls `__str__` by name. Trace `add1(x)`: starting from
`Program._run`, list the methods that run, in order, and say what causes each
`__str__` to be called.

### ANSWER

```
Replace this line with your answer.
```

**(d)** `sub1(x, 3)` is accepted, and `plcc-rep` prints it back. Nothing in
`V0` says `sub1` takes exactly one operand. If you wanted that to be an
error, **which section** of the specification would have to change — the
syntactic or the semantic — and what would the error look like to the user
in each case? (You do not have to make the change; say what it would take.)

### ANSWER

```
Replace this line with your answer.
```

**(e)** Run `3 + 4` through `plcc-rep` this time. It prints `3` on one line
and an error on the next. Explain both lines: why `3` was printed at all, and
what the parser was looking at when it gave up. (The `plcc-parse` output
from (a) shows the same thing as two trees; explain how they line up.)

### ANSWER

```
Replace this line with your answer.
```


## Before you run `save`

- [ ] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [ ] `q3/sum.plcc` — with your `More.sum` written, and the diff clean.
- [ ] You ran `save`. **Nothing is submitted until you have**, and it is safe
      to run as often as you like.

`plcc-ng/` directories are build caches. Leaving them in place costs you
nothing.
