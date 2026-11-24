# S029: Empty Ontology

A `.dlf` file that holds only a comment and declares nothing.

## The mistake

`model.dlf` contains this and nothing else:

```dolfin
# Notes for later: model the library here.
```

## What the checker says

`radeau check` reports a package warning:

```
⚠ Ontology 'https://www.dolfin.fr/examples/semantic-errors/s029-empty-ontology.model' (model.dlf) has no declarations
```

The package summary shows 0 concepts, 0 properties and 0 rules.

## How to fix it

Add at least one declaration (a concept, property, fact or rule) to `model.dlf`, or delete the file if you don't need it.
