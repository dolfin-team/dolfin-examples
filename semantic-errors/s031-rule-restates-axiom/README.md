# S031: Rule Restates Axiom

A rule copies something the model already says with the `symmetric` keyword.

## The mistake

```dolfin
concept Person:
  has friend: any Person
    symmetric

rule friendsym:
  match:
    ?a friend ?b
  then:
    ?b friend ?a
```

`symmetric` already means "if A is a friend of B, B is a friend of A". The package turns on OWL reasoning (`reasoning rdfs, owl`), which applies it. The rule `friendsym` adds nothing.

## What the checker says

```
warning[S031]: rule `friendsym` is redundant: `friend` is declared symmetric
  --> ./model.dlf:7:1
  = suggestion: Delete rule `friendsym`
```

## How to fix it

Delete the rule. Keep `symmetric` on `friend`.
