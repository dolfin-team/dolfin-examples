# S006: Unbound variable

This rule uses a variable in `then:` that `match:` never binds.

## The mistake

```dolfin
rule busy_owner:
  match:
    ?owner a Owner
  then:
    ?pet a BusyOwner
```

`?owner` is bound by `match:`. `?pet` is not, so the rule has no value to use for it.

## What the checker says

```
error[S006]: unbound variable `?pet` in the `then` block of rule `busy_owner` — it is not bound by the `match` block
  --> ./model.dlf:13:5
```

It also warns that `?owner` and `?pet` each appear only once.

## How to fix it

Bind every variable in `match:`, then use it in `then:`. For example:

```dolfin
rule busy_owner:
  match:
    ?owner a Owner
  then:
    ?owner a BusyOwner
```
