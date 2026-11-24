# schema.org Shop

The schema.org `Product`, `Offer` and `Organization` vocabulary written in Dolfin, plus a small fictional shop catalogue. Because of `@iri_name <https://schema.org/>`, the data comes out as plain schema.org.

## What's inside

- **`schema.dlf`**: a subset of schema.org as concepts: `Thing`, `Organization`, `Brand`, `Product`, `Offer`, `AggregateRating`, `PostalAddress`.
- **`ItemAvailability`, `OfferItemCondition`**: fixed lists (`one of:`) such as `InStock` or `RefurbishedCondition`.
- **`catalog.dlf`**: fictional organizations, brands and 12 products (lamps, chairs, bikes...), each with one or more offers and a rating.
- **`queries.md`**: four SPARQL queries to paste into the SPARQL tab.
- **`comparison.md`**: the same `Product` in schema.org's Turtle and in Dolfin, side by side.

## Try it

- Run query 1 in `queries.md` for the cheapest in-stock offer per product.
- Run query 3 to list refurbished or used offers.
- Open `catalog.dlf` and read the `lamp` fact: its `schema.weight` is `quantity(1.2 kg)`. Change `kg` to `m` and the checker flags it (S008), because a length is not a mass.

## Learn more

- Cardinalities: `one`, `optional`, `some` (for example `has offers: some Offer`).
- `@iri_name` to publish under an existing vocabulary namespace.
- Typed quantities with units, like `quantity(1.2 kg)`.
