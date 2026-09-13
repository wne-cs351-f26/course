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

**The two sandboxes** we used in class, `demo-plcc-parse` and `demo-plcc-rep`,
are the same material with the tool in front of you. Work through both before
starting. Every question below assumes you have.

### What you will be able to do

1. **Place the three phases.** Say what each of scanning, parsing, and
   semantic analysis takes in and hands on, and, given an error message, say
   which phase produced it.

2. **Predict what the parser does.** Given a grammar and an input, say whether
   the input parses and draw the tree it produces. Given a rejected input,
   say where the parse stopped and what it expected.

3. **Read a grammar rule as a class.** For any rule, name the class it
   defines, say whether it is abstract or a subclass, and list its attributes
   with their names and types — then check yourself with `plcc-diagram`.

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
  an LL(1) conflict, the error names the rules and the fix.

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

## QUESTION 1

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


## QUESTION 2

Repeat the question above, except use the following grammar rule:

```
<many> **= THIS <rule> HAS MULTIPLE OCCURRENCES <OF> <stuff>
```

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 3

Repeat the question above, except use the following grammar rule:

```
<classes> ::= I AM TAKING <CSIT>c1 <CSIT>c2 AND <CSIT>c3
```

### ANSWER

```
Replace this line with your answer.
```


## QUESTION 4

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


## QUESTION 5

In `q5/spec.plcc`, define a grammar that generates a parser that accepts strings that only contain a balanced set of parentheses, and end in an at-sign.

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

`q5/spec.plcc` contains a partial implementation of the language. So far, it contains a complete lexical specification. Your job is to complete the syntactic specification.

Your first rule should begin...

```
<Balanced> ::=
```

The legal and illegal input files have been provided for your convenience in `a2/q5/inputs/`.

> **Development Cycle**
>
> Same shape as the scanner loop in A1, but this time you need to test the
> parser.
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

## QUESTION 6

Going meta... In `q6/spec.plcc`, build a grammar for PLCC's lexical specification.
This is the syntactic counterpart to the scanner you wrote in A1.
Please ensure that your grammar embodies the following structure.

* Each line is either a comment or a rule.
* Each rule is either a skip rule or a token rule.
* The keyword "token" in a token rule is optional.

`q6/input` holds a small lexical specification to test your grammar against.
`plcc-parse` should exit 0 on it:

```bash
plcc-parse < input > /dev/null && echo PASS || echo FAIL
```

To try it on more input, copy the lexical section of any PLCC specification
into a file like `input2` -- delete everything from the first `%` onward --
and see whether your parser accepts it.


## QUESTION 7

This builds on question 6. Copy your `q6/spec.plcc` to `q7/spec.plcc`.
Add a semantic specification to `q7/spec.plcc` that
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


## QUESTION 8 (LONN)

Starter files

```
q8/lonn.grammar
```

LONN is a language for a nonempty-list-of-numbers. Implement the
minimum-value semantics for this language. That is, when a LONN program
is evaluated, it displays the minimum value in the list.
Here is an example `rep` session.

```
--> (    3 )
3
--> (3 5    2 4)
2
--> ()
ERROR (the default error message by PLCC)
```

You should test your implementation by running `rep` program with example
input. I recommend creating an input file to hold your test programs
and then redirect it into rep so that you can quickly and easily rerun
your tests.

Notice that LONN grammar defines a list of numbers recursively. That is,
when parsed, a list of numbers has a recursive structure. That means your
semantics implementation will use functional recursion to traverse this
structure and compute a value.


## QUESTION 9 (BINARY)

In `q9/binary.grammar`, write a lexical specification and semantics for
unsigned binary numbers. The meaning of this language is decimal value
of the given binary number. Here is an example `rep` session.

```
--> 0
0
--> 101
5
--> 000000011
3
--> 10000
16
--> 11111
31
--> 012
ERROR
```

Your lexical specification should have exactly three tokens: `NL` (a newline)
defined as `'\n'`, and binary digits `ZERO` and `ONE`.

I've given you a start on the syntactic specification. You will need to add
two grammar rules for the `<bit>` non-terminal, with RHS entries `ZERO` and
`ONE`, respectively, along with names of the subclasses of the Bit class to
accommodate the fact that there are two grammar rules with `<bit>` on their
left-hand sides.  You will need to choose those subclass names.

Once you have the lexical and syntactic specification complete, test them
using `parse -t`.

Add semantics to your grammar file by defining the following methods:

* A `$run()` in `Binary` that prints the results of `bits.eval()`.
* An `eval()` for `Bits` that runs through each `Bit` in `bitList`,
      calls their `eval()`, calculates the decimal value, and returns
      the result as an int.
* Declare an abstract `eval()` on `Bit` that returns an int.
* Define `eval()` that returns an int in the two subclasses of `Bit`;
      one of these should return 0, the other should return 1.

Use the following algorithm to calculate the binary value of the given
bits (do not use any libraries to do the work for you).

Use an accumulator pattern to calculate the decimal value. Initialize
`sum` to 0. Then loop through the bits from left to right. On each
pass of the loop, multiply the current sum by 2 and then add the current
bit to the sum. Here's example of converting 1011011 binary to 91 decimal:

```
running sum     =         0 (initial value)
                         /
                   _____/
                  /
1       base 10 = 0*2+1 = 1
^                     ^  /
                   _____/
                  /
10      base 10 = 1*2+0 = 2
 ^                    ^  /
                   _____/
                  /
101     base 10 = 2*2+1 = 5
  ^                   ^  /
                   _____/
                  /
1011    base 10 = 5*2+1 = 11
   ^                  ^  /
                   _____/
                  /
10110   base 10 =11*2+0 = 22
    ^                 ^  /
                   _____/
                  /
101101  base 10 =22*2+1 = 45
     ^                ^  /
                   _____/
                  /
1011011 base 10 =45*2+1 = 91
      ^               ^
```

If the `bitList` is empty (check its size), the `eval()` method should throw a
`PLCCException` with a message indicating that there are no digits.
