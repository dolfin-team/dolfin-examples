# S019: Conflicting field IRI

Two concepts both declare a field `p`, but give it different `@iri_name` values.

## The mistake

```dolfin
concept A
  has p: A
    @iri_name <http://x.org/p>

concept B
  has p: A
    @iri_name <http://x.org/q>
```

All fields with the same name are one property. One property cannot have two IRIs.

## What the checker says

```
error[S019]: field `p` already has the IRI <http://x.org/p>: all fields of one name are one property
  --> ./model.dlf:8:3
```

## How to fix it

Use the same `@iri_name` on both fields, or rename one field so they are separate properties.
