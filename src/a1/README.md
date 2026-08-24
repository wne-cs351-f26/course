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

## QUESTION 1

`a1/q1` contains the following starter files.

- `spec.plcc` - An empty file which you will modify.
- `input` - Sample input for the scanner. (Do not modify)
- `expected` - Expected output when scanner is given `input`. (Do not modify)

In `spec.plcc`, write a lexical specification acceptable to PLCC that skips over whitespace and skips all characters from a '#' character to the end of the line.  The lexical specification should accept the following strings as specific tokens:

```
this
that
the
other
thing
```

All other strings consisting of letters, digits, and underscores should be returned as a single ID token.  You should use appropriate token class names for the other tokens. If you encounter anything that does not conform to these specifications, it's an error.

`input` contains the following input for the scanner (Scan):

```
# example input
this that # the other thing
otherwise the thing
that is another thing
other#other#other#other
thisthat the end99 12345xxx _!
```

`expected` contains the expected output when the scanner is ran on `input`.

```
-:2:1 THIS 'this'
-:2:6 THAT 'that'
-:3:1 ID 'otherwise'
-:3:11 THE 'the'
-:3:15 THING 'thing'
-:4:1 THAT 'that'
-:4:6 ID 'is'
-:4:9 ID 'another'
-:4:17 THING 'thing'
-:5:1 OTHER 'other'
-:6:1 ID 'thisthat'
-:6:10 THE 'the'
-:6:14 ID 'end99'
-:6:20 ID '12345xxx'
-:6:29 ID '_'
-:6:30: error: unrecognized character '!'
```

> **DEVELOPMENT LOOP**
>
> To set up, position your terminal in the directory that
> contains the `spec.plcc` file you want to work on.
> Then do the following:
>
> 1. Run the scanner and compare its output with `expected`.
>     ```bash
>     plcc-scan < input | diff - expected
>     ```
>     No output from `diff` means they match. There is no separate compile
>     step: PLCC-ng builds the scanner for you and rebuilds it whenever
>     `spec.plcc` changes.
>
> 2. Modify `spec.plcc`, and repeat.


## QUESTION 2

In `q2/spec.plcc`, write a lexical specification for PLCC's lexical specification.
We are getting "meta" here. We want a scanner that can identify the tokens
for PLCC's lexical specification language. For example.

```
token HI 'hi'
skip BYE 'bye'
# comments too
```

> **Tip:** a PLCC pattern is normally delimited by single quotes, which makes
> matching a *literal* single quote awkward. You may delimit a pattern with
> double quotes instead, which is the easy way to match a quoted regex:
>
> ```
> token REGEX "'[^']*'"
> ```
