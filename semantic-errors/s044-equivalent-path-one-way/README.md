# S044: Equivalent path, inferred one way only

This project declares a property as equivalent to a path of other properties. That equivalence only works in one direction.

## The mistake

```dolfin
concept Person
property parent: Person -> Person
property grandparent: Person -> Person
  equivalent to parent / parent
```

`grandparent` is defined as "`parent` then `parent`". A reasoner can infer `grandparent` from two `parent` links. It cannot go the other way: a bare `grandparent` fact does not give you the two `parent` links, because the middle person is unknown.

## What the checker says

`radeau check` reports no linting issues on this project. The one-way behaviour is a modelling pitfall, not a syntax error.

## How to fix it

Do not expect `grandparent` facts to produce `parent` facts. State the `parent` facts and let `grandparent` be inferred from them.
