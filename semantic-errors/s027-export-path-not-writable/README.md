# S027: Export path not writable

An export maps a query result to a JSON key, but the key `"$..name"` is not a plain dotted path.

## The mistake

```dolfin
export
  from query report
  map:
    "$..name" as ?name
  to:
    <export://report.json> as JSONPath
```

`..` is a "search anywhere" operator. It can be read, but it cannot be used to write a value.

## What the checker says

```
error[S027]: "$..name" is not writable: a JSON export key is a dotted path like "$.a.b"
  --> ./model.dlf:18:5
```

## How to fix it

Use a dotted path with one dot per level:

```dolfin
    "$.name" as ?name
```
