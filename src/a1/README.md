# CS351 - Assignment a1

## Purpose

Two things are happening in this assignment.

The first is infrastructure. By the end of it you will have done the entire
loop once — opened your repository in Codespaces, fetched an assignment with
`begin`, worked on it, and submitted it with `save`. Every later assignment
assumes that loop works, so this one is deliberately light on content to leave
room for getting it right. If something is going to go wrong with your setup,
it is much better that it goes wrong now.

The second is the first real idea of the course: **how text becomes something a
computer can act on.** A language has *syntax* — the notation you write — and
*semantics* — what that notation means. Getting from one to the other happens
in three phases:

1. **Lexical analysis** (scanning) chops the character stream into tokens.
2. **Syntactic analysis** (parsing) assembles those tokens into a structure.
3. **Semantic analysis** walks that structure and does something.

This assignment is entirely about the first phase. That is not a warm-up before
the real material — scanning is where you learn that a language is a thing you
can *specify* rather than a thing you are handed, and everything after it is
built on that idea.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[Introduction](https://ourplcc.github.io/course-materials-ng/dev/00-introduction/),
[Overview](https://ourplcc.github.io/course-materials-ng/dev/01-overview/),
[Tokens](https://ourplcc.github.io/course-materials-ng/dev/02-tokens/), and
[PLCC](https://ourplcc.github.io/course-materials-ng/dev/03-plcc/). They are
short.

The Tokens chapter assumes you can read and write regular expressions. If you
are rusty, work [RegexOne](https://regexone.com/) lessons 1 through 9 before
starting. It takes under an hour and it is the single best use of your time on
this assignment.

### What you will be able to do

1. **Work in the course environment and submit through it.** Open your
   repository in Codespaces, run `begin` to fetch an assignment, and run `save`
   to submit one. Know that work is not submitted until `save` has run.

2. **Explain how this course works** — what the syllabus commits to, and how
   your homework is scored.

3. **Place lexical analysis in the pipeline.** Distinguish a language's syntax
   from its semantics, say what scanning does, and say what it hands to the
   phase after it.

4. **Predict and construct regular expressions.** Given a pattern, say which
   strings it matches. Given strings that should match and strings that should
   not, write a pattern that separates them.

5. **Read, run, and extend a lexical specification.** Write `token` and `skip`
   rules, run `plcc-scan` in all three invocation modes — a file argument,
   interactively, and with input redirected — read what it prints, and add new
   tokens to a specification that already works.

6. **Explain what the scanner does when more than one rule could match.**

### The core concepts

These are what the Correctness criterion looks at. Details — a clumsy regex, an
awkward token name, a rule you could have written more simply — are worth a
comment from me but cost you nothing. These are what matter:

- **Syntax versus semantics**, and where lexical analysis sits between them.
- **Token versus lexeme.** A token is a category; a lexeme is the actual text
  that matched it. When `plcc-scan` prints `-:1:1 NUM '1'`, `NUM` is the token
  and `'1'` is the lexeme.
- **`skip` versus `token`.** Both kinds of rule must *match* the input. The
  difference is only that a `skip` rule does not emit anything. Whitespace does
  not disappear because the scanner ignores it — it disappears because you
  wrote a rule that matches it and throws it away.
- **How ties are resolved.** The longest match wins. When two rules match the
  same longest text, the one written first wins. This is why a rule for a
  specific word has to appear *before* the general rule that would also match
  it.
- **What a lexical error is.** Not "the scanner got confused" — it is the
  specific situation where no rule matches at all, and it is the scanner
  correctly telling you your specification does not describe this input.

If you want to watch the tie-breaking happen rather than take my word for it,
run `plcc-scan -t`. It prints every rule that matched, how long each match was,
and which one it picked.

### Where this leads

A2 picks up the next two phases, on the same toolchain: you will write grammars
that turn tokens into structure, and semantics that walk that structure. The
specifications get longer but the workflow does not change, which is the other
reason this assignment spends its budget on getting the workflow solid.

On exams, this material shows up as questions you can only answer by having
built something — which strings a pattern matches, a pattern that separates two
sets, what a scanner does with an ambiguous input. Not by having memorized the
command names.

## QUESTION 1 — How this course works

Read [GRADING.md](https://github.com/wne-cs351-f26/course/blob/main/GRADING.md).
Then answer both parts. One or two sentences each.

**(a)** A student attempts every problem. Their work is complete and correct.
They run `save` four days after the due date. What is the best score they can
earn out of 9, and which single criterion costs them the most?

### ANSWER

```
Replace this line with your answer.
```

**(b)** I leave a comment on your submission suggesting a cleaner way to write
one of your regexes. How many points does that comment cost you?

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 2 — Where scanning sits

Short answers. One or two sentences each.

**(a)** In your own words, what is a language's *syntax*, and what is its
*semantics*?

### ANSWER

```
Replace this line with your answer.
```

**(b)** Lexical analysis is the first of three phases. What does it produce,
and what consumes what it produces?

### ANSWER

```
Replace this line with your answer.
```

**(c)** A token is an abstraction; a lexeme is an instance of it. Give one
token that could have many different lexemes, and one token that has exactly
one possible lexeme.

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 3 — Lab: build a scanner one rule at a time

This is a guided lab. Work the steps **in order** and answer as you go — the
later steps depend on what the earlier ones show you.

`q3/` contains three files.

- `spec.plcc` — empty. You will build it up over the course of this lab.
- `input` — sample input. **Do not modify.**
- `expected` — the output your finished scanner must produce. **Do not modify.**

`input` contains:

```
# example input
this that # the other thing
otherwise the thing
that is another thing
other#other#other#other
thisthat the end99 12345xxx _!
```

Position your terminal in `q3/` before you start. There is no compile step:
PLCC-ng rebuilds the scanner whenever `spec.plcc` changes.

Where you are going: whitespace skipped, `#` to end of line skipped, the five
words `this that the other thing` recognised as their own tokens, every other
run of letters/digits/underscores an `ID`, and anything else an error.

---

### Step 1 — Run it before you write anything

`spec.plcc` is empty. Run:

```bash
plcc-scan < input
```

**Report** the first three lines of output, and say in one sentence what an
empty specification does to the input.

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 2 — One rule

Put a single line in `spec.plcc`:

```
token ID '\w+'
```

Run it again. Some things are now tokens; a lot of it is still errors.

**Report** what is now recognised and what is not. Then answer: the spaces
between words were never something you wanted, so **why are they errors
rather than simply ignored?**

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 3 — Throw something away on purpose

Add a rule that skips whitespace. Run again.

**Report** what changed, and what is still an error.

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 4 — Comments

Add a rule that skips from a `#` to the end of the line. Run again.

You should now get through the whole file with no errors except one, at the
very end. Every word should be coming out as an `ID`.

**Report** your two `skip` rules. Then answer: line 5 of the input is
`other#other#other#other` — how many tokens does it produce, and why?

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 5 — Three ways to feed it

`plcc-scan` takes its input three ways: as a file argument, interactively from
the keyboard, and by redirection. Run your current specification all three
ways.

```bash
plcc-scan input          # file argument
plcc-scan                # interactive; type a line, then Ctrl-D
plcc-scan < input        # redirection
```

**Answer:** two of the three agree and one differs, in the same place on every
line. Which one differs, what is different, and why does that make sense?

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 6 — Add the keywords in the wrong place first

Add five `token` rules for `this`, `that`, `the`, `other`, and `thing`, using
the token names `THIS`, `THAT`, `THE`, `OTHER`, and `THING`. Put all five
**below** your `token ID` rule.

**Predict before you run.** Write down what you expect the word `this` on line
2 to come out as. Then run it.

#### ANSWER — your prediction, then what actually happened

```
Replace this line with your answer.
```

---

### Step 7 — Move them, and find out why it mattered

Move the five keyword rules **above** the `token ID` rule. Run again. The
keywords now come out as themselves.

But look at line 3. The word `otherwise` is still an `ID` — it did not become
`OTHER` followed by an `ID`. Two different things are going on, and this step
is about telling them apart.

Run the tracer and read the candidate table:

```bash
plcc-scan -t < input
```

**Answer both:**

**(a)** For the word `this`, two rules match and both match four characters.
Which rule wins, and what decides it?

**(b)** For the word `otherwise`, two rules also match. Which wins, and what
decides it *this* time? Would reordering your rules change this one?

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 8 — The error at the end

The input ends with `_!`.

**Predict** what your scanner does with those two characters, then run it and
check.

**Answer:** why is `!` an error? Your specification is not broken — say what
an error actually means here, and name one rule you could add that would make
`!` stop being one.

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 9 — Match the expected output

Your scanner should now reproduce `expected` exactly, error line included.

```bash
plcc-scan < input | diff - expected
```

No output from `diff` means they match.

**Report:** paste your finished `spec.plcc`. Leave it in `q3/spec.plcc` — this
is the file that gets graded.

#### ANSWER

```
Replace this line with your answer.
```

---

### Step 10 — On your own

Everything up to here told you what to do. This step does not.

Copy your working specification to a second file so you do not disturb step 9:

```bash
cp spec.plcc extra.plcc
```

Add a rule to `extra.plcc` that recognises a run of digits as a token named
`NUM`. Run it against the original input using the `-s` option, which points
`plcc-scan` at a specification other than the default:

```bash
plcc-scan -s extra.plcc < input
```

**Answer all three:**

**(a)** Compare the output to step 9's. What changed?

**(b)** The input contains `end99` and `12345xxx`, both of which contain
digits. Explain why your new rule did not do what you might have expected to
either of them.

**(c)** Write a line of input that makes `NUM` actually appear in the output,
and show the output that proves it.

#### ANSWER

```
Replace this line with your answer.
```
