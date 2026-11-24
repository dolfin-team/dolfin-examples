# S032: List value on a non-list field

The fact `a1` writes `list(...)` for `tag`, but `tag` is declared as a single string, not a list.

## The mistake

```dolfin
concept Article:
  has tag: any string

fact a1 a Article
  tag list("rdf", "owl")
```

## What the checker says

```
error[S032]: `tag` is not a `list of` field: write its values as `tag a, b`
  --> ./model.dlf:7:7
```

## How to fix it

Write the values separated by commas:

```dolfin
fact a1 a Article
  tag "rdf", "owl"
```

If you want an ordered list, declare the field as a `list of` type instead.
