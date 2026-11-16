# schema.org Product: Turtle vs Dolfin

schema.org publishes its vocabulary as RDF. Here is `Product` and two of its
properties, as schema.org itself writes them:

```turtle
schema:Product a rdfs:Class ;
    rdfs:label "Product" ;
    rdfs:subClassOf schema:Thing .

schema:sku a rdf:Property ;
    rdfs:label "sku" ;
    schema:domainIncludes schema:Offer, schema:Product ;
    schema:rangeIncludes schema:Text .

schema:offers a rdf:Property ;
    rdfs:label "offers" ;
    schema:domainIncludes schema:Product ;
    schema:rangeIncludes schema:Offer .
```

The same thing in Dolfin, with cardinalities that Turtle leaves unstated:

```dolfin
concept Product:
  sub Thing
  has sku: one string
  has offers: some Offer
```

And a product, as a shop would publish it:

```dolfin
fact lamp a schema.Product
  schema.name "Nautile desk lamp"
  schema.sku "NAU-LAMP-01"
  schema.weight quantity(1.2 kg)
  schema.offers [
    schema.price 89.0
    schema.priceCurrency "EUR"
    schema.availability schema.InStock
  ]
```

`quantity(1.2 kg)` is dimension-checked: the editor flags
`schema.weight quantity(1.2 m)` (diagnostic S008), because a length is not a mass.
