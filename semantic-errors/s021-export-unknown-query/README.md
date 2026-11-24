# S021: Export from an unknown query

An `export` block points at a query name that does not exist (a typo: `reprot` instead of `report`).

## The mistake

```dolfin
query report:
  ?_s a Student
    number ?num
    name ?name
  return
    Number ?num
    ?name

export
  from query reprot
  to:
    <export://report.csv> as CSV
```

## What the checker says

```
error[S021]: `reprot` is not a query of this package or its imports
  --> ./model.dlf:16:14
```

## How to fix it

Use the real query name: `from query report`.
