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

