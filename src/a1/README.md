# CS351 - Assignment a1

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


## QUESTION 3

Consider the following grammar rule in a PLCC file:

```
<blah>:Goo ::= THIS <VAR> IS <silly>
```

What (non-abstract) Java class does this grammar rule define, and what are its
instance variables (a.k.a. fields) and types?  Write your answer in the form of
a Java signature for the constructor for the class:

```
XXX(AAA aaa, BBB bbb, ...)
```

Here XXX is the class name, and the instance variables are aaa of type AAA, bbb
of type BBB, and so forth.

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 4

Repeat the question above, except use the following grammar rule:

```
<many> **= THIS <rule> HAS MULTIPLE OCCURRENCES <OF> <stuff>
```

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 5

Repeat the question above, except use the following grammar rule:

```
<classes> ::= I AM TAKING <CSIT>c1 <CSIT>c2 AND <CSIT>c3
```

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 6

Consider what is wrong with the following grammar rule in a PLCC file.  You can
assume that this is part of a larger PLCC grammar file in which other token
specifications and grammar rules may appear.  Your answer should be a grammar
rule that fixes all of the obvious errors on this line and that will be
acceptable to PLCC. Your answer should keep the essential nature of the
original grammar rule.

Do *not* add or remove any of the '<' or '>' characters. Do *not* try to
explain your answer -- just give the corrected grammar rule.

```
<VAR> := token <foo>
```

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 7

In `q7/spec.plcc`, define a grammar that generates a parser that accepts strings that only contain a balanced set of parentheses, and end in an at-sign.

For example, the following are legal sentences in the proposed language.

```
@
()@
()(()(()))@
```

The following are illegal sentences in the proposed language.

```
())@
(@
)(@
(()@
()
```

`q7/spec.plcc` contains a partial implementation of the language. So far, it contains a complete lexical specification. Your job is to complete the syntactic specification.

Your first rule should begin...

```
<Balanced> ::=
```

The legal and illegal input files have been provided for your convenience in `a1/q7/inputs/`.

> **Development Cycle**
>
> Same as in q1, but this time you need to test the parser.
>
> `plcc-parse` reports success or failure through its **exit status**: 0 when
> the input parses, non-zero when it does not. Do not judge by what is printed
> -- `plcc-parse` streams the parse tree as it goes, so a failing input still
> prints part of a tree before it reports the error.
>
> ```bash
> # Each of these should print PASS.
> plcc-parse < inputs/legal-01 > /dev/null && echo PASS || echo FAIL
>
> # Each of these should print FAIL.
> plcc-parse < inputs/illegal-01 > /dev/null && echo PASS || echo FAIL
> ```
>
> If you get tired of repeating these tests over and over again, consider writing a script to do it for you.

* Constraint: ***Do not*** use the repeating rule (`**=`).
* Tip: You should be able to define your grammar in just three BNF lines using two non-terminals.
* Tip: Do use recursion.
* Tip: You may need to provide PLCC with class names and/or field names to
  avoid collisions. Two captured symbols with the same name on one right-hand
  side is an error; write `<Nonterm:name>` to give one an explicit name.
* Tip: Recursion with an empty alternative is the shape you are looking for.
  Here is that idea applied to a *different* language -- a parenthesised list
  of numbers:

    ```
    <Lon>            ::= LPAREN <Nums> RPAREN
    <Nums:NumsNode>  ::= <NUM> <Nums>
    <Nums:NumsNull>  ::=
    ```

## QUESTION 8

Going meta again... In `q8/spec.plcc`, build a grammar for PLCC's lexical specification.
Please ensure that your grammar embodies the following structure.

* Each line is either a comment or a rule.
* Each rule is either a skip rule or a token rule.
* The keyword "token" in a token rule is optional.

You can use the input for q2 to test your grammar. `plcc-parse` should exit 0
on it:

```bash
plcc-parse < ../q2/input > /dev/null && echo PASS || echo FAIL
```

To try it on more input, copy the lexical section of any PLCC specification
into a file like `input2` -- delete everything from the first `%` onward --
and see whether your parser accepts it.


## Question 9

This builds on question 8. Copy your `q8/spec.plcc` to `q9/spec.plcc`.
Add a semantic specification to `q9/spec.plcc` that
creates a pretty-printer for a lexical specification.
Your pretty-printer
will reproduce the original input without comments, and with any `token`
keywords that were not present. For example, if the input was

```
skip WS '\s+'
# I have too much to do, so I'm not going to use the token keyword.
HI 'hi'
# OK, I have time to type this one.
token BYE 'bye'
```


When you run this through your interpreter (pretty-printer), it would
produce.

```
skip WS '\s+'
token HI 'hi'
token BYE 'bye'
```

We write semantics in **Python**. The semantic section comes after the second
`%`, and its first non-blank line names the language:

```
%
Python
YourStartSymbol
%%%
def _run(self):
    ...
%%%
```

Two rules to keep in mind:

* `_run` must **return** the output as a string. PLCC-ng prints it for you --
  do not print from inside `_run`.
* For polymorphism to work, every alternative you dispatch on needs its own
  version of the method you are calling. Python needs no abstract placeholder
  on the base class, but it will fail at run time if an alternative is missing
  the method.

Run your pretty-printer with `plcc-rep`:

```bash
plcc-rep < input | diff - expected
```
