# S048: Now-bound unsupported operator

This project puts a `[ != $y ]` bound on a property, but the operand is another property, not a literal value. Such a bound is not enforced.

## The mistake

```dolfin
concept Range:
  has low: float
  has high: float [ != $low ]
```

`high` is meant to differ from `low`. The bound refers to `$low`, which is not a literal.

## What the checker says

```
warning[S048]: `[ != $low ]` on `high` is not enforced: `!=` bounds are not supported with a non-literal operand
  --> s048-now-bound-unsupported-operator/model.dlf:5:21
  |
5 |   has high: float [ != $low ]
  |                     ^^^^^^^
```

## How to fix it

Use `!=` with a literal value, for example `[ != 0.0 ]`. To compare two fields, use another operator or a rule.
