# S051: Mapping source warning

A mapping loops over `$.venues[*]`, but that path matches nothing in `venues.json`, so no facts are produced.

## The mistake

```dolfin
mapping from <package://venues.json> as JSONPath
  for each "$.venues[*]"
  map:
    "$.location.city" as ?city
  to:
    fact <http://loc.example.com/city/{?city}> a ex:City
```

The file has a `venue` array, not `venues`.

## What the checker says

```
Mapping diagnostics:
  ⚠ iteration path '$.venues[*]' matched nothing
  0 row(s) skipped
```

It is a warning, not an error. The package still loads, but the mapping yields no `ex:City` facts.

## How to fix it

Use the key the file really has:

```dolfin
  for each "$.venue[*]"
```
