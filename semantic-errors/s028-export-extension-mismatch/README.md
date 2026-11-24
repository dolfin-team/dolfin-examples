# S028: Export extension mismatch

This project exports a query as XLSX but names the file `report.csv`.

## The mistake

```dolfin
export
  from query report
  to:
    <export://report.csv> as XLSX
```

The format says XLSX. The file name says CSV.

## What the checker says

```
warning[S028]: `report.csv` is written as XLSX: its extension should be `.xlsx`
  --> ./model.dlf:18:5
```

## How to fix it

Make the extension match the format. Rename the target to `report.xlsx`, or change the format to CSV.

```dolfin
<export://report.xlsx> as XLSX
```
