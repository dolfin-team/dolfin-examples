# S045: now() is incomparable

This project compares `now()` (a point in time) with an `int` bound. The two types can't be compared, so the constraint never holds.

## The mistake

```dolfin
concept Ticket:
  has n: one int [ <= now() ]
```

`n` is an `int`. `now()` returns the current time, not a number.

## What the checker says

```
error[S045]: `n` is type int: it never compares with `now()`
  --> s045-now-incomparable/model.dlf:4:20
  |
4 |   has n: one int [ <= now() ]
  |                    ^^^^^^^^
  = help: `now()` compares with a `date_time`, and with its UTC date / time-of-day part for a `date` / `time` field
```

## How to fix it

Bound a time field with `now()`, or bound the number with a number:

```dolfin
  has n: one date_time [ <= now() ]
```
