# S030: OWL reasoning off

This project declares a `transitive` property, but `package.dlf` sets `reasoning rdfs`. OWL reasoning is off, so the axiom does nothing.

## The mistake

```dolfin
concept Person:
  has ancestor: Person
    transitive
```

```dolfin
reasoning rdfs
```

## What the checker says

```
warning[S030]: `ancestor` is transitive but OWL reasoning is off: chained links won't be inferred
  --> ./model.dlf:5:5
  = help: add `owl` to the `reasoning` line of package.dlf
```

## How to fix it

Add `owl` to the `reasoning` line in `package.dlf`. Then a grandparent's ancestor is inferred as an ancestor too.
