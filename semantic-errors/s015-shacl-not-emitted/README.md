# S015: SHACL check not emitted

A `check` on `Crowd` uses a variable, `?nowhere`, that nothing binds. The SHACL emitter cannot express it, so the check is not validated.

## The mistake

```dolfin
concept Crowd:
  has member: Person
  check
    [ at_least ?nowhere member ]
```

`at_least` needs a number. Here it gets `?nowhere`, a variable that is never defined.

## What the checker says

`radeau check` reports no linting issues on this project. The problem shows up later. When Dolfin exports SHACL shapes, it skips this check. Your data is never tested against it.

## How to fix it

Give `at_least` a concrete number, or bind the variable first. For example:

```dolfin
check
  [ at_least 1 member ]
```
