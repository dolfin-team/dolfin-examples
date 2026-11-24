# S020: N3 not emitted

A `count` rule that also matches a second property (`weight`) of the counted thing, so the checker can't translate it to N3.

## The mistake

```dolfin
rule busy_owner:
  match:
    ?owner a Owner
    count ?pet as ?n
      ?pet owner ?owner
      ?pet weight ?w
  then:
    ?owner a BusyOwner
```

The `count` block also reads `?pet weight ?w`. If a pet has several weight rows, it would be counted once per row.

## What the checker says

```
warning[S020]: `count ?pet` in rule `busy_owner` has no N3 encoding: the rule runs as SHACL-AF only (validation), not in N3/retox reasoning or Agrafe SPARQL queries
  --> ./model.dlf:14:5
```

## How to fix it

Remove the extra `?pet weight ?w` line from the `count` block, so it only matches `?pet owner ?owner`. Each pet is then counted once.
