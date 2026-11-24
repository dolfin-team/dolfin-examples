# Real Estate Listings

A small data model for property listings: agents, properties, listings and buyer offers. It also shows two rules that tag data automatically.

## What's inside

- **`PropertyType`** and **`ListingStatus`**: fixed lists of values (`one of:`), such as `HOUSE` or `UNDER_OFFER`.
- **`Agent`**: a licensed agent, identified by `licenseNumber`.
- **`Property`**: a dwelling with address, bedrooms, bathrooms, size and an `agent`.
- **`Listing`**: a property for sale, with a status and an asking price in cents.
- **`Offer`**: a buyer's bid on a listing, with an `accepted` flag.
- **Sample facts**: `janAgent`, `riverHouse`, `riverHouseListing` and `firstOffer`.

## Try it

- Read the rule `flag_luxury`. It tags any `Property` over 3000 square feet as a `LuxuryProperty`.
- Read the rule `flag_stale_listing`. It tags every `ACTIVE` listing as a `StaleListing`.
- Run the query `accepted_offers`. It finds offers where `accepted` is true. The sample `firstOffer` is not accepted, so it returns nothing until you add one.

## Learn more

- `one of:` enumerations
- Rules with `match:` and `then:`
