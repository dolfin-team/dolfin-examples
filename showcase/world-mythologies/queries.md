# World mythologies — showcase queries

Paste into the SPARQL tab of the public project.

## 1. Deities of death, across traditions

```sparql
PREFIX m: <https://www.dolfin.fr/showcase/world-mythologies/mythologies#>
SELECT ?tradition ?figure WHERE {
  ?f m:domain m:Domain_Death ; m:name ?figure ; m:tradition/m:name ?tradition .
} ORDER BY ?tradition ?figure
```

## 2. Every descendant of Gaia (any depth)

```sparql
PREFIX m: <https://www.dolfin.fr/showcase/world-mythologies/mythologies#>
SELECT ?descendant WHERE {
  m:gaia m:parentOf+ ?d .
  ?d m:name ?descendant .
} ORDER BY ?descendant
```

## 3. Which domains appear in the most traditions?

```sparql
PREFIX m: <https://www.dolfin.fr/showcase/world-mythologies/mythologies#>
SELECT ?domain (COUNT(DISTINCT ?t) AS ?traditions) (GROUP_CONCAT(DISTINCT ?name; separator=", ") AS ?figures) WHERE {
  ?f m:domain ?d ; m:tradition ?t ; m:name ?name .
  BIND(STRAFTER(STR(?d), "_") AS ?domain)
} GROUP BY ?domain ORDER BY DESC(?traditions) ?domain
```

## 4. Legendary weapons and their wielders

```sparql
PREFIX m: <https://www.dolfin.fr/showcase/world-mythologies/mythologies#>
SELECT ?artifact ?wielder ?tradition WHERE {
  ?a a m:Artifact ; m:name ?artifact ;
     m:wieldedBy [ m:name ?wielder ; m:tradition/m:name ?tradition ] .
} ORDER BY ?tradition
```
