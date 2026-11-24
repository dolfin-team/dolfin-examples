# S022: Export maps a variable the query does not return

An `export` maps a column to `?grade`, but the query `report` never returns `?grade`.

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
  from query report
  map:
    N as ?num
    Grade as ?grade
  to:
    <export://report.csv> as CSV
```

## What the checker says

```
error[S022]: ?grade is not returned by query `report`
  --> ./model.dlf:19:5
   |
19 |     Grade as ?grade
   |     ^^^^^^^^^^^^^^^
```

## How to fix it

Either return the value from the query, or remove the `Grade as ?grade` line. For example, add a `grade` property to `Student`, bind `?grade` in the query, and list it under `return`.
