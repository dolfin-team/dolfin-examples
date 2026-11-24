# S025: Export to a bad target

An `export` block writes to a normal web URL instead of an `export://` file.

## The mistake

```dolfin
export
  from query report
  to:
    <http://example.org/report.csv> as CSV
```

## What the checker says

```
error[S025]: an export writes to an `export://` file, not <http://example.org/report.csv>
  --> ./model.dlf:18:5
```

## How to fix it

Use an `export://` file as the target. For example, `<export://report.csv> as CSV`. (The exact path form is a guess. I didn't test it.)
