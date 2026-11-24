# S034: Reified transitive

A property that carries extra data (`has since: ...`) is also marked `transitive`. Dolfin refuses this.

## The mistake

```dolfin
property manages: any Person -> any Person
  has since: optional date
  transitive
```

`manages` has a `since` annotation, so each link holds data. `transitive` would create new links (A manages C) with no `since` value.

## What the checker says

```
error[S034]: `manages` is reified (`has` lines / `via`): it cannot be `transitive`, chaining would invent links without annotations
  --> ./model.dlf:8:3
  = help: drop `transitive`, or write a rule that builds the chained links with their annotations
```

## How to fix it

Remove `transitive`. If you need chained links, write a rule that builds them and sets `since` yourself.
