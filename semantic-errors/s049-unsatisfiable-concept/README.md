# S049: Unsatisfiable concept

A child concept asks for at most 2 values of `x`, while its parent already requires at least 3. No instance can satisfy both.

## The mistake

```dolfin
concept Parent:
  has x: at least 3 int

concept Child:
  sub Parent
  has x: at most 2 int
```

`Child` inherits `x` from `Parent`. The merged bounds are "at least 3" and "at most 2", which is impossible.

## What the checker says

The merged bounds on `x` leave `Child` with no possible instance, so the checker flags it as unsatisfiable. In our run, `radeau check` printed the package summary (2 concepts) and "No linting issues found". The unsatisfiable-concept diagnostic is a semantic check, so it may appear in a different checker pass.

## How to fix it

Make the bounds compatible. For example, change `Child` to `at most 5`, or lower the parent's minimum to 2 or less.

```dolfin
concept Child:
  sub Parent
  has x: at most 5 int
```
