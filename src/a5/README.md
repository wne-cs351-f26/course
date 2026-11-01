# CS351 - Assignment a5

## Purpose

A4 ended with two answers to one question: when a procedure is called, what
does its formal get bound to? `SET` gives every formal a new ref holding a
copy. `REF` gives a variable argument's formal that variable's own ref. This
assignment adds three more answers. `NAME` and `NEED` delay an argument: the
formal gets the expression itself, evaluated later, when the body reads it.
The third, **copy-in, copy-out** (`CICO`), is not in the textbook or the
sandbox. You build it yourself, starting from `REF`, following the steps in
Question 2.

The main skill is still tracing. One skill is new: changing an interpreter so
that it has a semantics you can state in one sentence. When a run surprises
you, point to the line of the interpreter that caused it. In `CICO`, you wrote
that line.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[NAME](https://ourplcc.github.io/course-materials-ng/dev/16-name/) and
[NEED](https://ourplcc.github.io/course-materials-ng/dev/17-need/).
Copy-in, copy-out is not in the textbook. Question 2 teaches it.

**The `languages` sandbox** (`begin languages`) has `SET`, `REF`, `NAME`, and
`NEED`, ready to run. If your copy has no `NAME` or `NEED` directory, run
`begin -f languages` to get a fresh one. Nothing in the sandbox is submitted.

### What you will be able to do

1. **Trace a delayed argument.** Predict what a program prints in `NAME` and
   in `NEED`, and say when, and how often, each thunk is evaluated. Draw a
   thunk with the environment it keeps.

2. **Build a parameter-passing semantics.** Change `REF` into `CICO` and test
   it against programs whose output you predicted first.

3. **Compare five semantics.** For one program, classify each argument,
   predict the result in `SET`, `REF`, `NAME`, `NEED`, and `CICO`, and explain
   every difference.

### The core concepts

The Correctness criterion looks at these concepts. Details, such as the
layout of your diagram, may get a comment from me but cost you no points.

- **In `NAME`, an argument that is not a variable, a literal, or a `proc`
  becomes a thunk.** A thunk holds the unevaluated expression and the
  **caller's** environment. It is not text pasted into the body: a name in it
  is looked up where the call was made.

- **A thunk is evaluated every time its formal is read**, and never if the
  formal is never read.

- **In `NEED`, a thunk is evaluated at most once.** The first read evaluates
  it and saves the value. Every later read returns the saved value. So the
  value is fixed at the first read, not at the call.

- **In `NEED`, a formal bound to a literal or a `proc` is read-only too.** A
  formal can be `set` only if the caller passed a variable.

- **In `CICO`, a variable argument is copied in at the call and copied out at
  the return.** The formal gets a new ref holding a copy of the variable's
  value, taken when that argument is evaluated. Arguments are evaluated left
  to right, so a later argument that changes the variable does not change the
  copy. When the body finishes, the formal's final value is copied back into
  the variable's ref, one argument at a time, left to right. Any other
  argument is passed by value, and nothing is copied back.

- **During a `CICO` call, the variable and the formal are separate refs.** A
  change through one is not seen through the other until the return, and the
  copy-out then overwrites whatever the variable holds.

- **Aliasing is one ref reachable by two names.** For example, `.p(x, x)`, or
  a body that changes `x` directly while `x` is also an argument. In `REF` the
  two names share one ref, so each sees the other's changes at once. In `CICO`
  each name has its own copy, and the last copy-out wins.

- **Each semantics is a row of one table.** The columns are the kinds of
  argument: a variable, a literal, a `proc`, and anything else. In `REF`,
  `NAME`, and `NEED`, a variable is passed by reference and a literal or
  `proc` by value. `NAME` and `NEED` make anything else a thunk, which cannot
  be `set`. `CICO` is a fifth row. To predict a program, put each argument in
  its column and read the cell. In all five, `let` still makes a new ref
  holding a copy, and the arguments of a primitive like `+` are only read.

### Where this leads

Exam 2 asks you to do the same things you do here: classify each argument,
trace the program in more than one language, and say what prints and why.

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
the learning is. The run is only the check. A wrong prediction followed by an
honest correction is a complete answer.

**Every path in this handout is relative to `src/a5/`.** To run a program:

```bash
cd ../languages/NAME/python      # from src/a5/
echo 'let x = 3 f = proc(t) { t ; t ; t } in .f(set x = add1(x))' | plcc-rep
```

or run `plcc-rep` with no input and type or paste programs. Ctrl-D ends it.
Each question says which language to use. Running a program in the wrong one
is the most common way to get a surprising answer.

### Drawings

Question 1 asks for **one** drawing. Draw it by hand and submit it as an
image, as in A3 and A4. **[How to Hand In a Drawing](../../DRAWINGS.md)** says
how to name the file and where to put it.

Draw bindings as in A4: **name → ref → value**. Draw a **thunk** as we did
in class: a ref box holding the unevaluated expression, with an arrow from the
box to the node where the call was made.

Scoring is the same as in A1 to A4: [GRADING.md](../../GRADING.md), three
criteria, nine points. Correctness looks at the **core concepts** listed
above.

When you are done, run `save` from anywhere in your repository. **Your work is
not submitted until `save` has run.** It is safe to run as often as you like.


## QUESTION 1 — Call by name, call by need

**(a)** Run this in `SET`, `NAME`, and `NEED` (`../languages/SET/python`,
`../languages/NAME/python`, `../languages/NEED/python`):

```
let
  x = 0
in
  let
    f = proc(a, b) { a ; a ; +(a, x) }
  in
    .f(set x = add1(x), set x = 100)
```

Predict all three, then run all three. For `NAME` and `NEED`, say how many
times each argument's expression is evaluated, and what `x` holds just after
each read of `a`. For `SET`, say when the two `set`s run.

### ANSWER — (a)

```
Replace this line with your answer.
```

**(b)** Use `NAME`:

```
let
  y = 2
in
  let
    g = proc(t) let y = 100 in +(t, y)
  in
    let
      y = 5
    in
      .g(*(y, 3))
```

There are three `y`s. Predict, then run. Draw the environment `+(t, y)` is
evaluated in, as `q1b`, and write the file name in the answer block. Also draw
the node that holds `y = 5` and the nodes it links to, even though they are
not on that chain, so your thunk's arrow has somewhere to go.

Then explain the output: when `t` is read, which `y` does `*(y, 3)` use, and
why not either of the other two?

### ANSWER — (b)

```
Replace this line with your answer.
```

**(c)** Run both of these in `NAME` and in `NEED`:

```
let p = proc(n) { set n = *(n, 2) ; n } in .p(21)
let x = 21 p = proc(n) { set n = *(n, 2) ; n } in { .p(x) ; x }
```

Predict all four, then run all four. One of the four runs is an error. In
`../languages/NEED/python/spec.plcc`, find the class whose `setRef` raises
it, and quote that method. Then explain why the other program, which also
runs `set n`, works in `NEED`.

### ANSWER — (c)

```
Replace this line with your answer.
```


## QUESTION 2 — Build copy-in, copy-out

**Copy-in, copy-out** (`CICO`; also called *call by value-result*) works like
this. When an argument is a variable, the formal gets a **new** ref holding a
copy of the variable's value. That is the copy in, and it is the same as call
by value. The body then runs, and any `set` on the formal changes only that
copy. When the body finishes, the formal's final value is **copied back** into
the variable's ref. That is the copy out. When there is more than one
argument, the copies go back one at a time, left to right. An argument that is
not a variable is passed by value, and nothing is copied back for it.

The copy is taken when that argument is evaluated. Arguments are evaluated
left to right, so a later argument that changes the variable does not change
the copy.

Your starting point is `CICO/`, in this directory. It is a copy of `REF`, and
it runs as `REF` until you change it. **All your changes go in
`CICO/python/spec.plcc`.** Do not change `CICO/grammar.plcc` or `Env/`.
`CICO` uses `REF`'s grammar: the syntax is the same, only the behavior is
new.

To run it:

```bash
cd CICO/python      # from src/a5/
echo 'let x = 42 in { set x = add1(x) ; x }' | plcc-rep
```

The program used in (a) to (c) is:

```
let
  x = 5
in
  let
    p = proc(t) { set x = add1(x) ; set t = +(t, t) }
  in
    { .p(x) ; x }
```

**(a)** Before you change anything, predict what this program prints in `SET`
and in `REF`, then run both. Then, from the description above, predict what it
will print in `CICO`. Trace `x` and `t` through the call and the copy out.

### ANSWER — (a)

```
Replace this line with your answer.
```

Now build it, in four steps. Run the Question 2 program after every step.

**Step 1. Every ref can be copied out.** In the `Ref` section, add this
method to class `Ref`, after `setRef`:

```python
    def copyOut(self):
        pass
```

By default, copying out does nothing. `ValRef` inherits this, so an argument
that gets a plain `ValRef` is never copied back. Nothing has changed yet:
the program still prints what `REF` printed.

**Step 2. A ref for a variable argument.** Paste this between `ValRef`'s
closing `%%%` and the `ProcVal` line, with `VarRef` and both `%%%` lines at
the left margin. Then fill in the body of `copyOut`: one line, under the
comment, indented to match it (8 spaces).

```python
VarRef
%%%
from ValRef import ValRef


class VarRef(ValRef):

    def __init__(self, ref):
        super().__init__(ref.deRef())   # copy in: a new ref holding a copy
        self.ref = ref                  # the variable's own ref, kept for later

    def copyOut(self):
        # Put this ref's value back into the variable's own ref.
%%%
```

A `VarRef` *is* a `ValRef`: `deRef` and `setRef` work on its own copy, so a
`set` in the body never touches the variable. It also remembers the
variable's ref, so that `copyOut` can write to it.

**Step 3. Variable arguments get a `VarRef`.** In the `VarExp` section,
change `evalRef` so that it returns a `VarRef` built from the variable's ref,
instead of the variable's ref itself:

```python
def evalRef(self, env):
    return VarRef(env.applyEnvRef(self.symbol.lexeme))
```

and add an import section for it, just before the `VarExp` section:

```
VarExp:import
%%%
from VarRef import VarRef
%%%
```

**(b)** Run the program. It should print what `SET` printed. Why? You have
done the copy in. What has not happened yet, and so what does the variable
never see?

### ANSWER — (b)

```
Replace this line with your answer.
```

**Step 4. Copy out at the return.** In `ProcVal.apply`, the last line
returns the body's value immediately. Change it so that `apply` saves the
body's value, then calls `copyOut()` on every ref in `args`, in order, and
then returns the saved value.

**(c)** First check your build: `let x = 1 p = proc(t) set t = 7 in { .p(x) ; x }`
must print `7`. If it does not, compare your code with steps 1 to 4. Then run
the Question 2 program and compare its output with your prediction in (a).
Explain the output step by step: what `x` and `t` each hold after each `set`,
and what the copy out does to `x`.

### ANSWER — (c)

```
Replace this line with your answer.
```

**(d)** Change the call to `.p(+(x, 0))` and change nothing else. Predict,
then run in `CICO`. Explain the output: what kind of ref does `t` get, which
method made it, and what does its `copyOut` do?

### ANSWER — (d)

```
Replace this line with your answer.
```


## QUESTION 3 — Five ways to pass an argument

Use your `CICO` and the sandbox's `SET`, `REF`, `NAME`, and `NEED`.

**(a)** Here one variable is passed twice. Run both in `REF` and in `CICO`:

```
let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in .p(x, x)
let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in { .p(x, x) ; x }
```

Predict all four, then run all four. Explain each output from the refs: how
many refs do `a` and `b` have between them in each language? In `CICO`, what
does `x` hold after each copy out?

Then, without running anything: if `CICO` copied out right to left instead of
left to right, what would the second program print?

### ANSWER — (a)

```
Replace this line with your answer.
```

**(b)** In class we built a table: one row per language, one column per kind
of argument. Fill in the row for `CICO`. Where a word from the other rows
fits, use it. Where none fits, write the correct term.

| | variable `x` | literal `5` | `proc(y) y` | anything else: `add1(x)` |
| --- | --- | --- | --- | --- |
| **SET** | value | value | value | value |
| **REF** | reference | value | value | value |
| **NAME** | reference | value | value | thunk (evaluated on every read) |
| **NEED** | reference | value, read-only | value, read-only | thunk, cached (evaluated on first read only) |

Then run this in all five languages:

```
let
  x = 0
in
  let
    f = proc(a, b) { b ; set a = +(a, 100) ; +(b, x) }
  in
    .f(x, set x = add1(x))
```

Predict all five first. For each argument, say which column it is in, then
read your answer off that language's row. Then add `; x` after the call and
run it again in all five. Compare `CICO`'s call value and its final `x` with
`SET`'s and `REF`'s, and explain each difference from the refs.

### ANSWER — (b)

```
| | variable `x` | literal `5` | `proc(y) y` | anything else: `add1(x)` |
| --- | --- | --- | --- | --- |
| **CICO** |  |  |  |  |

Replace this line with your answer.
```


## Before you run `save`

- [ ] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [ ] Each answer says which language you ran it in, wherever the question
      used more than one.
- [ ] Your drawing, `q1b`, is in this directory, and its answer block names
      the file.
- [ ] `CICO/python/spec.plcc` has all four steps, and the Question 2 program
      prints what you said it would.
- [ ] You ran `save`. **Nothing is submitted until you have**, and it is safe
      to run as often as you like.

`plcc-ng/` directories are build caches. Leaving them in place costs you
nothing.
