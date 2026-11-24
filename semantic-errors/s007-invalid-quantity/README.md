# S007: Invalid Quantity

A fact gives a weight using a unit the checker does not know (`zonks`).

## The mistake

```dolfin
concept Parcel:
  has weight: mass

fact p1 a Parcel
  weight quantity(3 zonks)
```

`weight` is a `mass`, but `zonks` is not a real unit.

## What the checker says

```
error[S007]: invalid quantity literal: Unknown unit: zonks
  --> ./model.dlf:7:10
  |
7 |   weight quantity(3 zonks)
  |          ^^^^^^^^^^^^^^^^^
```

## How to fix it

Use a real mass unit. For example, kilograms:

```dolfin
  weight quantity(3 kg)
```
