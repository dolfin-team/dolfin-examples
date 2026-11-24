# S037: Sub-property of a reified property

A sub-property drops an annotation that its parent property requires.

## The mistake

```dolfin
property employs: any Company -> any Person
  has since: one date

property contracts: any Company -> any Person
  sub employs
```

`employs` needs a `since` date on every link. `contracts` is a kind of `employs`, but it does not say how to fill `since`.

## What the checker says

```
error[S037]: `contracts` is a sub-property of `model.employs`, which requires annotation `since`: its links would have no `since`
  --> ./model.dlf:10:3
   = help: reify it with the same `has` lines, or make the annotation `optional`
```

## How to fix it

Either repeat the annotation on the sub-property:

```dolfin
property contracts: any Company -> any Person
  sub employs
  has since: one date
```

Or make `since` optional on `employs`.
