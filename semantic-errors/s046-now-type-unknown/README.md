# S046: `now()` type unknown

This project compares `now()` with a field that the concept does not have.

## The mistake

```dolfin
concept Ticket:
  has due: one date
  check
    [ ghost [ <= now() ]]
```

`Ticket` only has `due`. The check uses `ghost`, which is not declared. So the type of the value compared with `now()` cannot be worked out.

## What the checker says

```
warning[S046]: cannot tell the type of `ghost`: `now()` is compared as a date_time; declare it with `has` in this concept
  --> s046-now-type-unknown/model.dlf:6:18
  |
6 |     [ ghost [ <= now() ]]
  |                  ^^^^^
```

## How to fix it

Compare a field the concept really has:

```dolfin
concept Ticket:
  has due: one date
  check
    [ due [ <= now() ]]
```
