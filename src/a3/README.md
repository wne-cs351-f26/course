# CS351 - Assignment a3

## Purpose

A2 ended with `V0`, a language that prints its program back. This assignment
covers the four languages that make programs **compute**: `V1` gives
expressions values, `V2` adds a choice, `V3` lets a program name its own
values, and `V4` adds procedures. What makes them work is the **environment**:
a chain of bindings that answers "what does this name mean here?"

Each language is the previous one plus one idea. So the skill this assignment
builds is tracing: given a program, say which environment each part is
evaluated in, what every name looks up to, and what comes out. When the
answer surprises you, say which line of the semantics is responsible.

This is the last assignment before Exam 1.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[Environments](https://ourplcc.github.io/course-materials-ng/dev/07-environments/),
[V1](https://ourplcc.github.io/course-materials-ng/dev/08-v1/),
[V2](https://ourplcc.github.io/course-materials-ng/dev/09-v2/),
[V3](https://ourplcc.github.io/course-materials-ng/dev/10-v3/), and
[V4](https://ourplcc.github.io/course-materials-ng/dev/11-v4/).

**The `languages` sandbox** (`begin languages`) has every one of these
languages, ready to run. Questions 1, 3, and 4 use it directly.

### What you will be able to do

1. **Draw the environment an expression is evaluated in.** For any `V1`–`V4`
   program, draw that environment's whole chain: every node, its bindings, its
   parent, and the environment any `ProcVal` in it saved.

2. **Predict what a program prints, and explain it from the chain.** Including
   shadowing, a name that is out of scope, and a right-hand side that sees the
   *old* binding.

3. **Add a primitive.** Extend a language with a new operator: the token, the
   grammar rule, and the `apply` method.

4. **Trace a procedure application.** Say what a `ProcVal` holds, which
   environment an application extends, and why a name that is free in a
   procedure's body finds the binding from where the procedure was *defined*.

### The core concepts

These are what the Correctness criterion looks at. Details, such as how your
diagram is laid out or whether you call a `proc` a function, are worth a
comment from me but cost you nothing. These are what matter:

- **An environment is a chain.** Each node holds bindings and points to its
  parent. Lookup starts at the node it is asked, stops at the first hit, and
  fails only at `EnvNull`. Nothing checks ahead of time that a name is bound:
  an unbound name fails only when it is looked up.

- **Only `let` and procedure application make new environments.** Primitives,
  `if`, and sequences evaluate in the environment they were given.

- **Operands are evaluated first.** Prims and procedures receive values:
  every operand is evaluated *before* `apply` runs. `if` is different. It
  evaluates only the branch it takes.

- **`let` evaluates every right-hand side in the old environment**, then
  binds them all at once in a new node that extends it. The body is evaluated
  in the new node. A binding can be seen only inside the body of its `let`:
  that is its **scope**. An inner binding of the same name **shadows** an
  outer one without changing it.

- **A binding names a value.** Nothing in `V1`–`V4` changes a binding.

- **A `proc` is a value that carries its environment.** A `ProcVal` holds the
  formals, the body, and the environment the `proc` was evaluated in. That
  is what makes it a **closure**. Applying it extends *that* environment, not
  the one it is called from.

### Where this leads

`V5` makes recursion part of the language instead of a trick you write by
hand, as in Question 4. `V6` and the languages after it let a program
*change* a binding. That is the first time the order of evaluation can change
the answer, and every idea in this assignment is what you will reason with
when it does.

On Exam 1, this material shows up as the same things you do here: draw the
environments, trace a program, say what prints and why.

## How to do this assignment

**Your answers go in this file.** Every question has one or more `ANSWER`
blocks that look like this:

````
```
Replace this line with your answer.
```
````

Replace that line with your answer and leave the fences around it alone.

**Predict first, then run.** Write the prediction down before you run
anything. Then run it and say whether you were right. The prediction is where
the learning is; the run is only the check. A wrong prediction followed by an
honest correction is a complete answer.

**Every path in this handout is relative to `src/a3/`.**

To run a program in a language from the sandbox:

```bash
cd ../languages/V3/python      # from src/a3/
echo 'let x = 3 in add1(x)' | plcc-rep
```

or run `plcc-rep` with no input and type or paste programs. A program can
span several lines, and `plcc-rep` starts the next program wherever the last
one ended. Ctrl-D ends it.

Question 2 has its own directory, `q2/`, laid out like the sandbox:
`grammar.plcc`, then `python/spec.plcc`. Run `plcc-rep` from the `python/`
directory. Edit only `q2/NEG/grammar.plcc` and `q2/NEG/python/spec.plcc`.
Leave `q2/Env/` alone: it is the environment code NEG includes.

### Drawings

Questions 1 and 4 ask you to **draw** environments. Draw them by hand, in the
notation from class, and hand them in as images. **Read
[How to Hand In a Drawing](../../DRAWINGS.md) first.** It says how to name the
files and where to put them, and it has four worked examples.

Every drawing question asks for **the environment some expression is evaluated
in**. Draw that environment's whole chain. The empty environment a `V3` or `V4`
program starts in is optional.

How this is scored is the same as A1 and A2: [GRADING.md](../../GRADING.md),
three criteria, nine points. The **core concepts** listed above are what
Correctness looks at.

When you are done, run `save` from anywhere in your repository. **Your work is
not submitted until `save` has run.** It is safe to run as often as you like.


## QUESTION 1 — Draw the chain

Use `V3` (`../languages/V3/python`). For (a), (b), and (d): **predict** what
the program prints, **draw the environment its innermost body is evaluated
in**, then run it and check the value. Name the drawing for the part, such as
`q1a.jpg`, and write the file name in the answer block.

**(a)**

```
let
  x = 3
  y = 5
  z = 8
in
  +(x,+(y,z))
```

### ANSWER — (a)

```
Replace this line with your answer.
```

**(b)**

```
let
  x = 3
in
  let
    y = 5
  in
    let
      z = 8
    in
      +(x,+(y,z))
```

### ANSWER — (b)

```
Replace this line with your answer.
```

**(c)** (a) and (b) print the same value, but they build different chains.
In **both** programs, change the right-hand side of `y` from `5` to
`add1(x)`, and change nothing else. Predict both, then run both. Explain the
difference using your drawings for (a) and (b). No new drawing is needed.

### ANSWER — (c)

```
Replace this line with your answer.
```

**(d)**

```
let
  q = 6
in
  let
    q = 60
    y = q
  in
    y
```

Draw the environment the innermost body, `y`, is evaluated in. Then quote
the **one line** of `LetDecls.addBindings` (in
`../languages/V3/python/spec.plcc`) that decides which `q` the right-hand side
sees, and say in a sentence what it does.

### ANSWER — (d)

```
Replace this line with your answer.
```


## QUESTION 2 — Add a primitive

`q2/NEG/` is a copy of `V1`. Before changing anything, run `neg(3)` in it:

```bash
cd q2/NEG/python      # from src/a3/
echo 'neg(3)' | plcc-rep
```

**(a)** It prints two lines. Explain both. What token did the scanner make
from `neg`? What did the parser think `neg` was, and why did the next program
fail at the `(`? Which phase produced each line?

### ANSWER — (a)

```
Replace this line with your answer.
```

**(b)** Add a `neg` primitive that takes one argument and returns its
arithmetic negative:

```
neg(add1(3))      % -4
neg(neg(42))      % 42
```

You will need a `NEGOP` token in `grammar.plcc`, a grammar rule for a
`NegPrim`, and an `apply` method for `NegPrim` in `python/spec.plcc`. The
other prims show you the pattern. Then answer: **where does the token go in
the lexical section, and why does its position matter?**

### ANSWER — (b)

```
Replace this line with your answer.
```

**(c)** Change the `LIT` token so a literal can begin with an optional minus
sign. With your change:

```
neg(-11)          % 11
add1(-12)         % -11
```

Then predict, and check, what `-(4,-1)` prints. There are two `-`
characters in it. Say which token each one becomes, and why the scanner
can tell them apart.

### ANSWER — (c)

```
Replace this line with your answer.
```

Paste your `NegPrim` section and your changed lines from `grammar.plcc` here,
as well as leaving them in the files.

### ANSWER — (code)

```
Replace this line with your answer.
```


## QUESTION 3 — Scope

Use `V3`. For each program: **predict** the output, then run it. Then
**explain** the output from the environment chain. A drawing is not required.
If one helps you explain, hand it in as [DRAWINGS.md](../../DRAWINGS.md)
says, named for the program, such as `q3a.jpg`.

```
(a)  let y = 5 in +(let y = sub1(y) in y, y)
(b)  let x = let y = 2 in add1(y) in y
(c)  let a = 2 in let b = a in let a = 50 in +(a, b)
(d)  let x = y y = 2 in x
(e)  let x = 1 x = 2 in x
```

For (e), name the method that raises the message.

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 4 — Procedures

Use `V4` (`../languages/V4/python`).

**(a)** Predict what this prints, then run it:

```
let
  n = 10
in
  let
    g = proc(k) *(k,n)
  in
    .g(4)
```

For the application `.g(4)`, draw the environment `g`'s body is evaluated
in, and the environment `.g(4)` itself is evaluated in, with the value of `g`.
Both go in one drawing, `q4a.jpg`, as in the last two examples in
[DRAWINGS.md](../../DRAWINGS.md). Then say in a sentence which environment
the application **extends**.

### ANSWER — (a)

```
Replace this line with your answer.
```

**(b)** Now add one more `let` between the definition and the application:

```
let
  n = 10
in
  let
    g = proc(k) *(k,n)
  in
    let
      n = 100
    in
      .g(4)
```

Predict and run. Draw the same two environments as in (a), in `q4b.jpg`.
Then point to the line in `ProcVal.apply` (in
`../languages/V4/python/spec.plcc`) that decides which `n` the body sees, and
say what one change to that line would make the program print the *other*
value you might have expected.

### ANSWER — (b)

```
Replace this line with your answer.
```

**(c)** A `let` is an applied `proc` in disguise. The textbook gives the rule:
`let V1 = E1 ... Vn = En in B` means the same as
`.proc(V1, ..., Vn) B (E1, ..., En)`. Rewrite each program below using the
rule so that it has **no `let`s**, and make no other change. Run the original
and your rewrite to check that they print the same value.

```
let
  x = 3
  y = 5
  z = 8
in
  +(x,+(y,z))
```

```
let
  x = 3
in
  let
    y = 5
  in
    +(x,+(y,2))
```

Hint for the second one: work from the inside out.

### ANSWER — (c)

```
Replace this line with your answer.
```

**(d)** This program looks like it should compute 4 factorial:

```
let
  fact = proc(x) if zero?(x) then 1 else *(x, .fact(sub1(x)))
in
  .fact(4)
```

Run it. Explain the error from **which environment the `ProcVal` saved**, and
why `fact` is not in it.

Then write `sumto`, which adds the numbers from `n` down to `0`, using the
textbook's workaround of passing the procedure to itself. This should
print `10`:

```
let
  sumto = ...
in
  .sumto(sumto, 4)
```

### ANSWER — (d)

```
Replace this line with your answer.
```

**(e)** Sequences. Predict, then run:

```
{ 1 ; 2 ; 3 }
{ /(1,0) ; 5 }
let x = 1 in { let x = 2 in x ; x }
```

Read `SeqExp.eval`. In `V4`, an expression before the last one in a sequence
can never change the answer, only stop it. Why? What would a language need
before those earlier expressions could matter?

### ANSWER — (e)

```
Replace this line with your answer.
```


## Before you run `save`

- [ ] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [ ] `q2/NEG/`: `neg` works, negative literals work, and your changes are
      pasted into Question 2.
- [ ] Your drawings, `q1a`, `q1b`, `q1d`, `q4a`, and `q4b`, are in this
      directory, and each answer block names its file.
- [ ] You ran `save`. **Nothing is submitted until you have**, and it is safe
      to run as often as you like.

`plcc-ng/` directories are build caches. Leaving them in place costs you
nothing.
