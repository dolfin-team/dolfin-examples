# S036: Symmetric cardinality mismatch

A `symmetric` property is declared with a different cardinality on each side.

## The mistake

```dolfin
property married: optional Person -> one Person
  symmetric
```

If A is married to B, then B is married to A. Both sides are the same kind of link. But one side says `optional` and the other says `one`.

## What the checker says

```
warning[S036]: `married` is symmetric but its domain cardinality (`optional`) differs from its range cardinality (`one`)
  --> ./model.dlf:7:3
  = help: a symmetric link counts the same both ways: give both sides the same cardinality
```

## How to fix it

Use the same cardinality on both sides:

```dolfin
property married: optional Person -> optional Person
  symmetric
```
