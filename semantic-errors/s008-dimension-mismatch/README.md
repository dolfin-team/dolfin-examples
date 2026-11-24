# S008: Dimension mismatch

This project gives a length to a property that expects a mass.

## The mistake

```dolfin
concept Parcel:
  has weight: mass

fact p1 a Parcel
  weight quantity(2 m)
```

`weight` is a mass, but `2 m` is a length (meters).

## What the checker says

```
error[S008]: dimension mismatch: `weight` expects a Mass quantity, found Length
  --> ./model.dlf:7:10
  |
7 |   weight quantity(2 m)
  |          ^^^^^^^^^^^^^
```

## How to fix it

Use a unit of mass, such as kilograms:

```dolfin
fact p1 a Parcel
  weight quantity(2 kg)
```
