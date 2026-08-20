# A5

## Q1

TYPE1/program contains a program written in SET but needs to be updated
to run in TYPE1. That program defines a proc named `compose` that takes
two procs. Each of these procs takes one integer argument
and returns an integer result. `compose` returns a new proc that composes
the passed procs. The returned proc takes an integer, applies one proc to
the integer getting a new integer, and then applies the other proc to that
integer to get another integer, which it returns.

Add type expressions to TYPE1/program so it passes TYPE1's type checker,
and runs correctly.

Recall, within the TYPE1 directory, you compile TYPE1 as follows:

```
plccmk -c grammar
```

And you run the program as follows:

```
rep program
```

After it prints its output, you'll be at a `rep` prompt: `-->`.
Press ctrl+D or ctrl+C to exit.

## Q2

What is the type of the following let expression?

```
let
  p = proc(f:[int=>int]):[int=>int] proc(x:int):int .f(.f(x))
  q = proc(t:int):int *(t,t)
in
  .p(q)
```

Give your answer as a type expression.

## Q3

```
your answer here
```

## Q4

What's wrong with the following expression in TYPE1?
Don't correct them. Just identify them.

```
if add1(0) then +(4,5) else {let p=proc():int 9 in p}
```


## ANSWER

```
your answer here
```

## Q5

Below are the list of type errors that TYPE1's checker detects. For each,
make an example in TYPE1 that demonstrates the error that TYPE1 will detect.
Remember you can test your answers in TYPE1. Write your example in the
code block provided.

* an attempt to define a procedure whose declared return type does not match the type of the body of the procedure;

    ```
    ```

* an attempt to apply a non-procedure as a procedure;

    ```
    ```

* an attempt to apply a procedure to the wrong number of actual parameters;

    ```
    ```

* an attempt to apply a procedure to actual parameters whose types do not match the declared types of the corresponding formal parameters;

    ```
    ```

* an attempt to use a non-boolean as the test in an if statement;

    ```
    ```

* an attempt to have expressions of different types in the then and else parts of an if statement;

    ```
    ```

* an attempt to assign a value to a LHS variable in a set expression where the type of the variable does not match the type of the RHS expression.

    ```
    ```

As an additional exercise (not to be submitted), correct each of the errors
that you created and confirm that it works.
