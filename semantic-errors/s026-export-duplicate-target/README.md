# S026: Export Duplicate Target

Two `export` blocks write the same file, `report.csv`.

## The mistake

```dolfin
export
  from query report
  to:
    <export://report.csv> as CSV

export
  from query report
  to:
    <export://report.csv> as CSV
```

## What the checker says

```
error[S026]: another export already writes `report.csv`
  --> ./model.dlf:23:5
```

The error points at the second `<export://report.csv>`.

## How to fix it

Give each export its own file name, for example `report.csv` and `report-copy.csv`. Or delete the duplicate export.
