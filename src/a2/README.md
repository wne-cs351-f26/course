# CS351 - Assignment A2

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
