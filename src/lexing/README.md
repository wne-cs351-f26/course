# Lexing in PLCC

The goal of this activity are:

* Ensure you have a working development environment for PLCC.
* Use PLCC to build scanners from a lexical specification in a grammar file.
* Ensure you can access your individual homework repository on GitLab
    and are able to submit work to it.

## Setup

1. Navigate to your personal repository for this course on GitLab.
2. Open your repository in GitPod by prefixing the repository URL with
    `https://gitpod.io/#`, so your repository URL follows the `#` in the
    full URL. Hit enter so the browser opens it.
3. Create the workspace with the default configuration. This should open
    a VS Code in your browser attached to a clone of your repository.
4. Test by entering the following in VS Code's terminal:

    ```bash
    plcc --version
    ```

    You should see the version number of plcc, and not an error.
5. Run `begin lexing` to get a copy of this activity.
1. Position your command-line in the `lexing/` directory.
    ```
    cd lexing
    ```

## Compiling and running a scanner interactively

`grammar` contains a lexical specification for a language.
Open it and familiarize yourself with it.

Let's compile and run the scanner.

1. Compile the grammar.
    ```
    $ plccmk -c grammar
    ```
2. Run the scanner. The scanner reads from standard input, which is the
    keyboard by default. So after you start the scanner, type some words
    on two or three lines and observe the scanner's output. Each time you
    press enter, the scanner scans the line and prints the tokens it
    recognizes.
    ```
    $ scan
    type some words
        1: WORD 'type'
        1: WORD 'some'
        1: WORD 'words'
    more word
        2: WORD 'more'
        2: WORD 'word'
    ```
    When you have had enough, press CTRL+D to send an EOF (end of file)
    character, or press CTRL+C to send a terminate signal.

Repeat the above, but this time enter some characters that the scanner
will not recognize and see what it does.

## Running a scanner on a file

More often we want to run our scanner on the contents of a file.
Let's run our scanner on `program`. This file represents a program
written in our new `words` language. We have already built the scanner
in the last section. So we just need to run our scanner and redirect
standard input to the contents of `program`. We do this using
`<` followed by the file name.

```
scan < program
```

Try the last command to see that it works.

Create a `program2` file and put some invalid "tokens" in it and scan it.

## Glance Under the Hood

Take a look at the files in `Java/`.
Open `Token.java` and find the definitions of the tokens from `grammar`.

`Scan.java` is the scanner. This is what you have been interacting with
when you ran `scan`. In fact, `scan` is a script that runs the compiled
`Scan.class` as follows

```
java -cp Java Scan
```

Try the above command and confirm that it behaves just as `scan` did.

## Exercise

Add a NUMBER token to grammar that matches non-negative integers like

```
0
56
234
```

Recompile the grammar. It's always a good idea to delete the Java folder
before you do.

```
$ rm -rm Java
```

This ensures that you always get the latest versions of all the Java and
class files.

Now run your new scanner on `program` to ensure it still works,
and that `program2` still fails.

Now create `program3` that uses your new token, and make sure it works.

## Save your work to GitLab

Run the following command

```
save "finished lexing activity"
```

Open a your personal project in GitLab and confirm that it contains your work.

## Stop the workspace

You must stop your GitPod workspace, or GitPod will continue charging your
credits for the next 30m. Run the following command to stop your workspace.

```
gp stop
```

## `save-and-stop`

You can both save your work to GitLab and stop GitPod in a single command
as follows.

```
save-and-stop "your message here"
```

Reopen your workspace, and try this command.
