# EV charging in the Rhône — showcase queries

Paste into the SPARQL tab of the public project. Each charge point is one
`ev:ChargePoint`; power values are typed quantities (`"22"^^unit:kW`), and
`xsd:decimal(STR(?p))` gives the number in kW. `ev:commune` is derived by the
`commune_by_*` rules of `charging.dlf`.

## 1. Installed capacity per operator

```sparql
PREFIX ev: <https://www.dolfin.fr/showcase/ev-charging/charging#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT (SAMPLE(?name) AS ?operator) (COUNT(DISTINCT ?s) AS ?stations)
       (COUNT(DISTINCT ?cp) AS ?chargePoints) (ROUND(SUM(xsd:decimal(STR(?p)))) AS ?totalKW) WHERE {
  { SELECT DISTINCT ?o ?s ?cp ?p WHERE { ?s ev:operator ?o ; ev:chargePoints ?cp . ?cp ev:power ?p } }
  ?o ev:name ?name .
} GROUP BY ?o ORDER BY DESC(?totalKW) LIMIT 15
```

## 2. Fast-charging sites (≥ 150 kW, CCS) open 24/7 in Lyon

```sparql
PREFIX ev: <https://www.dolfin.fr/showcase/ev-charging/charging#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?station (SAMPLE(?op) AS ?operator) (MAX(?kW) AS ?maxKW) (COUNT(DISTINCT ?cp) AS ?fastPoints) WHERE {
  ?s ev:name ?station ; ev:operator/ev:name ?op ; ev:openAllHours true ;
     ev:commune/ev:name "Lyon" ; ev:chargePoints ?cp .
  ?cp ev:power ?p ; ev:connectors ev:Connector_CCS .
  BIND(xsd:decimal(STR(?p)) AS ?kW)
  FILTER(?kW >= 150)
} GROUP BY ?station ORDER BY DESC(?maxKW) DESC(?fastPoints)
```

## 3. Communes with the most charge points

```sparql
PREFIX ev: <https://www.dolfin.fr/showcase/ev-charging/charging#>
SELECT ?commune (COUNT(DISTINCT ?cp) AS ?chargePoints) (COUNT(DISTINCT ?s) AS ?stations) WHERE {
  ?s ev:commune/ev:name ?commune ; ev:chargePoints ?cp .
} GROUP BY ?commune ORDER BY DESC(?chargePoints) LIMIT 10
```

## 4. Stations commissioned per year

```sparql
PREFIX ev: <https://www.dolfin.fr/showcase/ev-charging/charging#>
SELECT ?year (COUNT(?s) AS ?stations) WHERE {
  ?s ev:commissionedOn ?d .
  BIND(YEAR(?d) AS ?year)
} GROUP BY ?year ORDER BY ?year
```

## 5. Free-to-use charging, by site type

```sparql
PREFIX ev: <https://www.dolfin.fr/showcase/ev-charging/charging#>
SELECT ?siteType (COUNT(?s) AS ?freeStations) WHERE {
  ?s ev:freeToUse true ; ev:siteType ?t .
  BIND(STRAFTER(STR(?t), "_") AS ?siteType)
} GROUP BY ?siteType ORDER BY DESC(?freeStations)
```
