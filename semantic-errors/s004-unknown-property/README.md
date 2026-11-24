# S004: Unknown property

A fact sets a property (`year`) that its concept (`Book`) never declared.

## The mistake

```dolfin
concept Book:
  has title: string

fact dune a Book
  title "Dune"
  year 1965
```

`Book` only has `title`. The fact adds `year`, which does not exist.

## What the checker says

```
error[S004]: unknown property `year` in fact `dune`
  --> ./model.dlf:8:3
  = suggestion: Declare property `year: int` in `Book`
```

## How to fix it

Declare the property on the concept (or remove the line from the fact):

```dolfin
concept Book:
  has title: string
  has year: int
```
