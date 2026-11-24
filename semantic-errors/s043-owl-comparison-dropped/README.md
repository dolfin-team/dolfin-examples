# S043: OWL comparison dropped

A subconcept restricts a quantity with a comparison (`> 40 kg`). OWL cannot express that, so the comparison is meant to be left out of the OWL output.

## The mistake

```dolfin
concept Dog:
  has weight: mass

concept BigDog:
  sub Dog with weight: > quantity(40 kg)
```

## What the checker says

```
info[S043]: not expressible in OWL: left out of the OWL output; the rule and validation still check it
  --> s043-owl-comparison-dropped/model.dlf:7:11
  |
7 |   sub Dog with weight: > quantity(40 kg)
  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

This is information, not an error. The package builds.

## What it means

OWL has no way to say "weight above 40 kg", so the OWL output describes `BigDog` without that condition. Nothing is lost in Dolfin: the generated rule still classifies a heavy dog as a `BigDog`, and validation still checks the bound. Only an OWL reasoner reading the ontology on its own will not see it.
