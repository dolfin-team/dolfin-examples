# S010: Missing Required Value

A fact creates a `Book` but never gives it an `author`, which the concept requires.

## The mistake

```dolfin
concept Person
concept Book:
  has author: one Person

fact dune a Book
```

`one` means exactly one value is required. The fact `dune` sets none.

## What the checker says

```
error[S010]: missing required field `author` in fact `dune` (type `Book`)
  --> ./model.dlf:7:6
```

## How to fix it

Give the fact an author. For example, add a `Person` fact and set `author` on `dune`. Or, if an author is not always known, change the field to an optional one instead of `one`.
