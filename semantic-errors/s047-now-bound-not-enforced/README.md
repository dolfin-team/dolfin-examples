# S047: now() bound not enforced

This project puts a `now()` bound on a `list of` field. The bound looks like a rule, but it is not enforced.

## The mistake

```dolfin
concept Log:
  has at: list of date_time [ <= now() ]
```

The field `at` holds many date-times. The constraint `<= now()` is meant to forbid future dates. It does not check them.

## What the checker says

```
warning[S047]: `[ <= now() ]` on `at` is not enforced: `at` is a `list of` field: the bound reads the list, not its members
  --> s047-now-bound-not-enforced/model.dlf:4:31
  |
4 |   has at: list of date_time [ <= now() ]
  |                               ^^^^^^^^
  = help: write `list of (date_time [ … ])` to bound each element
```

## How to fix it

Put the bound inside the parentheses, so it applies to each element:

```dolfin
  has at: list of (date_time [ <= now() ])
```
