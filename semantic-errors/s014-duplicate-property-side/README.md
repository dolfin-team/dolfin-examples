# S014: Duplicate property side

A property gives its domain twice: once in the one-line form and again on a `domain` line.

## The mistake

```dolfin
property wrote: Person -> Book
  domain Person
```

`Person -> Book` already sets the domain (`Person`) and the range (`Book`). The extra `domain Person` line repeats it.

## What the checker says

```
error[S014]: the domain of property `wrote` is already given
  --> ./model.dlf:7:3
  |
7 |   domain Person
  |   ^^^^^^^^^^^^^
```

## How to fix it

Give each side once. Drop the `domain` line:

```dolfin
property wrote: Person -> Book
```
