# S039: Symmetric sides mismatch

A symmetric property links a `Person` to a `Company`, two different types. Symmetric means order does not matter, so both sides should have the same type.

## The mistake

```dolfin
concept Person
concept Company

property worksWith: any Person -> any Company
  symmetric
  has since: optional date
```

`worksWith` is symmetric and reified (it carries its own `since` field). But its domain is `Person` and its range is `Company`.

## What the checker says

```
warning[S039]: `worksWith` is symmetric and reified but its domain (`Person`) differs from its range (`Company`)
  = help: a symmetric link's source / target order means nothing: give both sides the same type
```

## How to fix it

Give both sides the same type, for example `property worksWith: any Person -> any Person`. Or drop `symmetric` if the direction matters.
