# Hospital pharmacy

The pharmacy of Hôpital Saint-Roch (fictional) dispenses drugs to four wards. Physicians prescribe
a drug with a dose, a frequency, a route, a start date and a duration, and the pharmacist dispenses
it from a batch. The model types every dose, stock and volume as a physical quantity. SHACL checks
incoming prescriptions and dispensings, and rules flag overdoses, expired batches and children
given drugs that have no pediatric dosing.

Data: 8 patients (Léa, Noah and Inès are pediatric), 10 drugs with real ATC codes,
15 batches (P-2312 and E-2406 expired), 20 prescriptions and 25 dispensings, all invented. The
comments next to the facts give the expected outcome of each tricky case: Inès is 14 and Malik
has just turned 18, some doses sit exactly at the maximum, and E-2406 was dispensed once before
it expired and once after.

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| Dimension-typed fields (`mass`, `volume`, `density`) | pharmacy.dlf:42, 80 | `sh:node [ sh:sparql … dq:dimension "M1" ]`; S008 on a wrong unit in a fact |
| `mg/mL` concentration (`density`) | pharmacy.dlf:272 | `"5"^^<https://dolfin.dev/unit/mg.mL-1>` |
| Unit conversion in a fact | pharmacy.dlf:451, 606 (`quantity(0.25 L as mL)`) | `"250"^^<…/unit/mL>` |
| Cross-unit comparison (1500 mg > 1 g) | pharmacy.dlf:122, 507 | N3 rule with `dq:lessThan` |
| `one` cardinality | pharmacy.dlf:78 (`prescriber`) | `sh:minCount 1 ; sh:maxCount 1` |
| Field bounds | pharmacy.dlf:73, 81 | `sh:minInclusive` / `sh:maxInclusive` |
| Derived field from `now()` | pharmacy.dlf:41 | `sh:SPARQLFunction` (SHACL), `dt:years` (retox) |
| `equivalent to` + condition | pharmacy.dlf:48 (`PediatricPatient`) | `sh:SPARQLRule` + `sh:sparql` |
| `check` with `$`-variables | pharmacy.dlf:92, 108 | `sh:sparql` (`SafePrescription: condition not met`) |
| Closed set with fixed keys | pharmacy.dlf:8 (`Ward`) | `Ward_PEDIATRICS` individuals with `code "PED"` |
| Rules, including `none` | pharmacy.dlf:122, 130, 138 | N3 rules (`log:notIncludes` for `none`) |
| Query with filters + `order` | queries.dlf:1 | `FILTER`, `ORDER BY` |
| `group by` + `count distinct` / `sum` | queries.dlf:13, 40 | `GROUP BY`, `COUNT(DISTINCT …)`, `SUM` |
| Query on inferred classes | queries.dlf:23, 61, 66, 72 | plain `SELECT` over the materialized data |
| `none:` | queries.dlf:50 | `FILTER NOT EXISTS` |

The checks live on `SafePrescription` and `SafeDispensing`, which are sub-concepts. The facts are
the ward's record, mistakes included, and the rules flag those mistakes. Data that is submitted for
dispensing asserts the safe concept, so its violations are reported under that concept's name.

## Commands

From `rust/`:

```sh
cargo run -q -p radeau -- check examples/showcase/hospital-pharmacy
cargo run -q -p radeau -- build examples/showcase/hospital-pharmacy --emit shacl -o /tmp/pharmacy-shacl.ttl
cargo run -q -p radeau -- validate examples/showcase/hospital-pharmacy --now 2026-06-15T12:00:00Z \
  --data examples/showcase/hospital-pharmacy/validate/bad/expired_batch.ttl
cargo run -q -p radeau -- validate examples/showcase/hospital-pharmacy --now 2026-06-15T12:00:00Z \
  --data examples/showcase/hospital-pharmacy/validate/known-bug/overdose.ttl   # conforms today: bug B
cargo test -p radeau --test showcase_examples
```

`validate/bad/` holds one violation per file: missing prescriber, a dose in mL, 30 doses a day and
an expired batch. `queries/expected/` was computed by hand from the facts.

## Limitations hit

The letters refer to the entries under "hospital-pharmacy showcase" in `rust/BUGS.md`.

- **A.** `quantity_on_hand` has no `[ >= 0 ]`. On a quantity field, both a plain literal bound
  (`[ >= 0 ]`) and a quantity bound (`[ >= quantity(0 mg) ]`) are accepted by `radeau check`, but
  each makes every value a violation. The bound is on `packs_on_hand: int [ >= 0 ]` instead.
- **B.** The `SafePrescription` check (dose ≤ the drug's maximum) compiles but never fails, because
  SHACL compares quantities as plain literals. `overdose.ttl` therefore sits in `validate/known-bug/`.
  Move it to `bad/` once B is fixed. Overdoses are still caught by the unit-aware rule
  `flag_overdose` (query `overdose_alerts`).
- **C.** `PediatricPatient` cannot be written as `[ some age [ < duration(18y) ] ]`, because that
  form reads `age` as a stored triple. It uses the CanVote form `[ ward [ adult_age [ > $age ] ] ]`,
  so each ward carries `adult_age duration(18y)`.
- **D.** A `date` never compares with a `date_time`. `Dispensing` therefore has a `day: date` next
  to `at: date_time`, and both the check and the rule compare `expiry` with `day`.
- **E.** `sum` over a quantity field (stock in g and kg) is unbound. `stock_by_drug` sums
  `packs_on_hand` instead.
- **F.** The weight-based pediatric check (dose > weight × mg/kg) is not modelled, because rule
  arithmetic on quantities never matches. `flag_unchecked_pediatric` covers the case where a drug
  has no mg/kg maximum at all. `pediatric_max_per_kg` is a plain `float` (mg/kg) because
  dolfin-units has no mass-per-mass dimension.
- `now()` is not available in queries, so `expiring_batches` uses the literal window
  2026-06-15 to 2026-09-13 (90 days after `validate/now`).
- Agrafe materializes rules with the wall clock, not `validate/now`. The expiry results do not
  depend on the clock, and Malik is adult at any clock after 2026-06-10. The pediatric results
  (`PediatricPatient`, and RX-04/RX-06 in `NeedsPharmacistReview`) hold until 2030-06-20,
  when Inès turns 18 (Léa and Noah stay minors until 2036 and 2039).
- The text report of `dose_wrong_dimension.ttl` shows `NodeConstraintComponent` with the message
  `Value does not conform to a Mass quantity (dimension M1)`.
