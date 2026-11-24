# S018: SHACL not checked

The package has a broken alias, so it never builds. The `check` on `Person` is never turned into SHACL.

## The mistake

```dolfin
concept Person:
  has age: int
  check
    [ age [ >= 0 ]]

alias Persn as Human
```

`Persn` is a typo. No concept or import with that name exists.

## What the checker says

```
Error: Package error: Alias 'Human' targets 'Persn', which no import defines and the package does not declare, in file './model.dlf'
```

Because the package fails, the `age >= 0` rule is never generated or enforced.

## How to fix it

Point the alias at the real concept:

```dolfin
alias Person as Human
```
