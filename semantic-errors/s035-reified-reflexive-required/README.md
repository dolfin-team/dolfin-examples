# S035: Reflexive property with a required annotation

A `reflexive` property carries a required annotation (`level: one int`). Reflexive means every `x` implicitly gets `x trusts x`, and those links have no value for `level`.

## The mistake

```dolfin
property trusts: any Person -> any Person
  has level: one int
  reflexive
```

## What the checker says

```
error[S035]: `trusts` is reflexive but its annotation `level` is required: the implied `x trusts x` links would have no `level`
  --> ./model.dlf:8:3
  = help: make the annotation `optional` or `any`, or drop `reflexive`
```

## How to fix it

Make the annotation optional, or drop `reflexive`.

```dolfin
property trusts: any Person -> any Person
  has level: optional int
  reflexive
```
