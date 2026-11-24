# EV charging in the Rhône

Public electric-vehicle charging stations in the Rhône department (France), built straight from open data. A Dolfin mapping reads the national IRVE CSV and a list of communes. No script is needed.

## What's inside

- **`Station`** and **`ChargePoint`**: a station has many charge points. Each point has a `power` (in kW) and `connectors` such as `Type2` or `CCS`.
- **`Operator`**: the company running a station. Rows with no operator are skipped.
- **`Commune`** and **`MunicipalDistrict`**: towns, plus Lyon's nine districts, each linked to Lyon with `partOf`.
- **`SiteType`** and **`Connector`**: fixed lists of values, like `OnStreet` or `FastChargingHub`.
- **Mappings**: one reads `communes-69.json`, one reads `irve.csv`. The CSV has one row per charge point, and the rows merge into one `Station` fact.
- **Rules** `commune_by_name`, `commune_by_district`, `commune_by_postal_code`: operators write the location in different ways. These rules work out each station's `commune`.

## Try it

- Open `charging.dlf` and read the `commune_by_postal_code` rule. It uses `none` to apply only when no verified commune name exists.
- Open `queries.md` and paste a query into the SPARQL tab. For example, "Installed capacity per operator" or "Fast-charging sites (≥ 150 kW, CCS) open 24/7 in Lyon".
- The download commands for `irve.csv` are at the top of `charging.dlf`.

## Learn more

- `one of:` enumerations and `case` to turn raw text into typed values.
- Typed quantities with `as quantity(kW)`.
- Rules with `none` (negation).
