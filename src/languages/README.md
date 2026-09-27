# CS351 - The languages, `V0` to `V6`

**Nothing here is graded and nothing here is submitted.** This is a sandbox:
the reference implementations of the languages we study, for you to run, read,
and change. When you want it back the way it started:

```bash
begin -f languages
```

That replaces this whole directory with a fresh copy, discarding whatever you
did to it. If you have changed a language and want to keep the change, copy
that language's directory somewhere else first.

## Running a language

Go to one implementation of a language and run `plcc-rep`. It builds the
language from `spec.plcc` and then reads programs from you, one after another.
Ctrl-D ends it.

```bash
cd V3/python
plcc-rep
```

```text
let x = 3 in let x = add1(x) y = add1(x) in +(x, y)
8
```

`V4/Prog/` and `V6/Prog/` hold example programs.

## How it is laid out

```text
V3/
  grammar.plcc          the lexical and syntactic specification
  python/spec.plcc      the semantics, in Python
  java/spec.plcc        the same semantics, in Java
  javascript/spec.plcc  the same semantics, in JavaScript
Env/                    environments, shared by every language
```

**A language's syntax is written once, and its meaning is written once per
implementation language.** Each `spec.plcc` begins with
`%include ../grammar.plcc`, so all three implementations parse exactly the same
programs. They differ only in the language the semantics are written in. We
work in Python. If you think more clearly in Java or JavaScript, the other two
implementations are there to read alongside it.

The environment classes are needed by every language from `V1` on, so they are
written once, in `Env/`, and each `spec.plcc` includes the one it uses. That is
why the includes reach up two directories. Move a `spec.plcc` somewhere else
and its includes break.

## Where this comes from

A copy of [ourPLCC/languages-ng](https://github.com/ourPLCC/languages-ng) at
tag `v1.0.0` — the version the textbook links to — with its automated tests
left out. It is licensed under the GNU GPL version 3; see `LICENSE`.
