# S016: Unstratifiable definitions

Two concepts are defined in terms of each other, and one of the links goes through a negation (`none`).

## The mistake

```dolfin
concept X:
  equivalent to Base
    [ none p [ a Y ]]

concept Y:
  equivalent to Base
    [ some p [ a X ]]
```

`X` means "no `p` leads to a `Y`". `Y` means "some `p` leads to an `X`". So `X` depends negatively on `Y`, and `Y` depends on `X`. That is a cycle through a negation.

## What the checker says

The intended diagnostic is S016 (unstratifiable). In our run, `radeau check` printed "No linting issues found" and did not report it. Check the project's package description for the intended error.

## How to fix it

Break the cycle. Define one concept without referring to the other, or remove the `none` from the loop.
