# S005: Invalid temporal literal

A `date` property is given a value written as a duration (`7d`).

## The mistake

```dolfin
concept Person:
  has birthDate: date

fact bob a Person
  birthDate date(7d)
```

`date(...)` expects a calendar date. `7d` means "7 days", which is a duration.

## What the checker says

```
error[S005]: invalid temporal literal: date(...) declared but value parses as a duration
  --> ./model.dlf:7:13
  |
7 |   birthDate date(7d)
  |             ^^^^^^^^
```

## How to fix it

Give `date(...)` a real date, or change the property's kind to match the value you mean. Run `radeau check .` to confirm the error is gone.
