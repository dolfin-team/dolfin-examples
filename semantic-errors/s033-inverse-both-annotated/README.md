# S033: Inverse pair with annotations on both sides

Two properties are declared as inverses of each other, and both carry `has` annotations.

## The mistake

```dolfin
property lends: any Person -> any Person
  has amount: one float

property borrows: any Person -> any Person
  has note: one string
  inverse of lends
```

An `inverse of` pair shares one link. Annotations (`amount` and `note`) cannot live on both sides.

## What the checker says

```
error[S033]: `borrows` and `model.lends` both declare `has` annotations: an `inverse of` pair shares one link
  --> ./model.dlf:11:3
   = help: declare the annotations on one side only
```

## How to fix it

Keep the annotations on one property only. For example, move `note` to `lends`, or drop it:

```dolfin
property lends: any Person -> any Person
  has amount: one float

property borrows: any Person -> any Person
  inverse of lends
```
