# S009: Unresolved reference

A fact gives a value that names nothing: there is no fact, enum member or concept called `nobody`.

## The mistake

```dolfin
concept Person
concept Book:
  has author: Person

fact dune a Book
  author nobody
```

`nobody` is never declared, so `author` points at nothing.

## What the checker says

```
error[S009]: `nobody` in fact `dune` is not a fact, enum member or concept of this package
  --> ./model.dlf:8:10
```

## How to fix it

Declare the fact, then refer to it:

```dolfin
fact nobody a Person

fact dune a Book
  author nobody
```

Or point `author` at a fact that already exists.
