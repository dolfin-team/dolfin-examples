# S023: Export modifier on a named query

This project puts `limit 3` inside the `map:` block of an export that uses `from query report`.

## The mistake

```dolfin
export
  from query report
  map:
    N as ?num
    limit 3
  to:
    <export://report.csv> as CSV
```

A named query already has its own `return`. Row limits belong there, not in the export's `map:`.

## What the checker says

```
error[S023]: `limit` belongs to the `return` of query `report`
  --> ./model.dlf:17:3
```

## How to fix it

Remove `limit 3` from `map:`. Put the limit in the `return` of `query report` instead.
