# S050: Mapping row skipped

A mapping reads a CSV file, but one row has an empty `id` cell, so that row is skipped.

## The mistake

The mapping needs `id` to build each fact's name (`st:{?id}`):

```dolfin
mapping from <package://stops.csv> as CSV
  map:
    id as ?id
    route as ?route
  to:
    fact st:{?id} a Stop
      route {?route} as int
```

In `stops.csv`, row 2 has no value for `id`.

## What the checker says

```
Mapping diagnostics:
  ⚠ row 2: empty value for required binding ?id
  1 row(s) skipped
```

It is a warning. The rest of the package still checks fine.

## How to fix it

Fill in the missing `id` in `stops.csv`. Or remove the row if it should not be there.
