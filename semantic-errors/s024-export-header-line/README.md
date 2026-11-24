# S024: Header line on a CSV export

This project puts a `sheet` line on a CSV export. `sheet` only makes sense for spreadsheet formats like Excel, so the checker rejects it.

## The mistake

```dolfin
export
  from query report
  to:
    <export://report.csv> as CSV
    sheet "Students"
```

A CSV file has no sheets, so the `sheet "Students"` line does nothing here.

## What the checker says

```
error[S024]: `sheet` does not apply to CSV exports
  --> ./model.dlf:19:5
   |
19 |     sheet "Students"
   |     ^^^^^^^^^^^^^^^^
```

## How to fix it

Remove the `sheet` line, or export to a format that has sheets.

```dolfin
export
  from query report
  to:
    <export://report.csv> as CSV
```
