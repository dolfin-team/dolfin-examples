# S001: Unresolved type

A concept names a parent type that is never declared, because of a typo.

## The mistake

```dolfin
concept Book

concept Novel:
  sub Bok
```

`Novel` says it is a sub-type of `Bok`. Only `Book` exists.

## What the checker says

```
error[L/semantic/unresolved-type]: Unresolved type 'Bok' in parent of 'Novel'. Did you mean 'Book'?
  --> ./model.dlf:6:7
  = suggestion: Replace with 'Book'
```

## How to fix it

Fix the spelling, or declare the missing type.

```dolfin
concept Novel:
  sub Book
```
