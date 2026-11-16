# schema.org shop — showcase queries

Paste into the SPARQL tab of the public project. Every term is plain
schema.org, so these queries run unchanged on any schema.org dataset.

## 1. Cheapest in-stock offer per product

```sparql
PREFIX schema: <https://schema.org/>
SELECT ?product ?bestPrice ?seller WHERE {
  { SELECT ?p (MIN(?price) AS ?bestPrice) WHERE {
      ?p a schema:Product ; schema:offers [ schema:price ?price ; schema:availability schema:ItemAvailability_InStock ] .
    } GROUP BY ?p }
  ?p schema:name ?product ;
     schema:offers [ schema:price ?bestPrice ; schema:availability schema:ItemAvailability_InStock ;
                     schema:seller/schema:name ?seller ] .
} ORDER BY ?bestPrice
```

## 2. Best-rated products with at least 100 reviews

```sparql
PREFIX schema: <https://schema.org/>
SELECT ?product ?brand ?rating ?reviews WHERE {
  ?p schema:name ?product ; schema:brand/schema:name ?brand ;
     schema:aggregateRating [ schema:ratingValue ?rating ; schema:reviewCount ?reviews ] .
  FILTER(?reviews >= 100)
} ORDER BY DESC(?rating)
```

## 3. Refurbished or used offers (second-hand catalogue)

```sparql
PREFIX schema: <https://schema.org/>
SELECT ?product ?price ?condition ?seller WHERE {
  ?p schema:name ?product ;
     schema:offers [ schema:price ?price ; schema:itemCondition ?c ; schema:seller/schema:name ?seller ] .
  FILTER(?c != schema:OfferItemCondition_NewCondition)
  BIND(STRAFTER(STR(?c), "_") AS ?condition)
} ORDER BY ?price
```

## 4. Catalogue size and price range per category

```sparql
PREFIX schema: <https://schema.org/>
SELECT ?category (COUNT(DISTINCT ?p) AS ?products) (MIN(?price) AS ?from) (MAX(?price) AS ?to) WHERE {
  ?p schema:category ?category ; schema:offers/schema:price ?price .
} GROUP BY ?category ORDER BY ?category
```
