# S038: Missing edge annotation

A fact uses a property that requires an annotation (`q`), but leaves it out.

## The mistake

```dolfin
property ingredient: any Recipe -> any Ingredient
  has q: one mass

fact pancake a Recipe
  ingredient flour
```

`ingredient` carries a required annotation `q` (a mass). The `pancake` fact links to `flour` without giving one.

## What the checker says

```
error[S038]: `ingredient` has required annotations: write `ingredient flour [q …]`
  --> ./model.dlf:11:14
```

## How to fix it

Give the edge a value for `q`, as the message suggests: `ingredient flour [q …]`, where `…` is a mass.
