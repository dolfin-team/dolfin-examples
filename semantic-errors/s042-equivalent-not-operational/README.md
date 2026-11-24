# S042: Equivalent Not Operational

An `equivalent to` definition uses `only`, so Dolfin generates no rule and no shape for it. The OWL output stays unchanged.

## The mistake

```dolfin
concept Kept:
  equivalent to Dog with owner: only Person
```

`only Person` means every owner must be a `Person`. Dolfin generates no rule and no shape from it, so `Kept` does nothing.

## What the checker says

`radeau check` shows no lint issue here (3 concepts, 1 property, 0 rules). The project is meant to show that the definition is not operational: no rule, no shape, OWL unchanged.

## How to fix it

Do not rely on `only` inside `equivalent to` to classify or validate anything. Write an explicit rule or shape for that constraint instead.
