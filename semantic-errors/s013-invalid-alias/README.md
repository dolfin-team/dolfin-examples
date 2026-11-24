# S013: Invalid alias

This project defines an alias that points at a name that does not exist.

## The mistake

```dolfin
concept Person

alias Persn as Human
```

`Persn` is a typo. No concept, import or declaration has that name.

## What the checker says

```
Error: Package error: Alias 'Human' targets 'Persn', which no import defines and the package does not declare, in file './model.dlf'
```

## How to fix it

Point the alias at a real name. Here, fix the typo:

```dolfin
concept Person

alias Person as Human
```
