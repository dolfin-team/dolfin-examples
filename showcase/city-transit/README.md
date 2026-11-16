# City transit: Réseau Lumière

Réseau Lumière (fictional) is the tram and bus network of a mid-size French city. Two teams keep its
data, in two packages:

- The infrastructure team owns `network/`: 25 stops with their fare zone and step-free access, five
  lines (trams T1, T2, T3, buses 10 and 11) and the stops each one serves, and walkways between nearby
  stops.
- The operations team owns `timetable/`. It **imports** `network` at a pinned version and adds the
  service journeys and their passing times, the vehicle types and the disruptions. Journeys and passing
  times come from a NeTEx-like XML export (`timetable/data/timetable.xml`), small, simplified and
  invented.

Four stops are interchanges: Gare Centrale (T1, T2, 10), Hôtel de Ville (T2, T3, 11), République
(T1, T3) and Université (T1, 11). Opéra, Colline Saint-Just and Vergers, all on bus 10, are not
step-free. At `now` (2026-06-23T07:45:00Z, a Tuesday morning, `timetable/validate/now`) roadworks at
Hôtel de Ville (D-0412, until further notice) are the only active disruption: one is over, two have
not started.

```text
 network/  <https://www.dolfin.fr/showcase/city-transit/network>  version 2.1.0
 ┌────────────────────────────────────────────────────────────┐
 │ infrastructure team                                        │
 │ Stop (key stop_code, lat/long, accessible, zone)           │
 │ Line (key code, mode, stops, length)  FareZone  Mode       │
 │ serves / served_by (inverse of)                            │
 │ connected_to (symmetric) ⊑ reachable_from (transitive)     │
 │ facts: 25 stops, 5 lines, 4 walkways                       │
 └───────────────▲────────────────────────────────────────────┘
                 │ import <…/network> "2.1.0"
                 │ lock: timetable/.dolfin/imports/<slug>/ (relock.sh)
                 │ prefix fr.dolfin.showcase.city_transit.network.network as net
 ┌───────────────┴────────────────────────────────────────────┐
 │ operations team                                            │
 │ ServiceJourney (line: net:Line)  PassingTime (stop: net:Stop)
 │ VehicleType  DayType  Disruption (affects: net:Stop)  Cause│
 │ checks: stop on the journey's line, low floor → step-free  │
 │ rules: DisruptedJourney, Interchange   5 queries           │
 │ data/timetable.xml → mappings.dlf: 12 journeys, 48 calls   │
 └────────────────────────────────────────────────────────────┘
 timetable/  <https://www.dolfin.fr/showcase/city-transit/timetable>  version 1.4.0
```

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| Package version | network/package.dlf:3 | `owl:Ontology` of the package |
| Import at a pinned version | timetable/package.dlf:6 | `owl:imports <https://www.dolfin.fr/showcase/city-transit/network>` |
| Prefix over an imported namespace | timetable/timetable.dlf:10, queries.dlf:1 | `@prefix net: <https://www.dolfin.fr/showcase/city-transit/network/network#>` |
| Imported types | timetable/timetable.dlf:45, 58, 82 (`net:Stop`, `net:Line`) | `sh:class net:Line`, `rdfs:range net:Line`: by IRI, not copied |
| Imported individuals in facts | timetable/timetable.dlf:135 (`affects net:HDV`) | `timetable:affects net:HDV` |
| IRI prefix in mapping templates | timetable/mappings.dlf:5, 21, 48 (`net:{?line}`) | `timetable:line net:T3` |
| Key fields | network/network.dlf:20, 32 | `owl:hasKey` + SHACL key rules |
| Bounded floats | network/network.dlf:24-25 | `sh:maxInclusive "90"^^xsd:integer`; the negative bound is dropped, see K |
| Dimension-typed field | network/network.dlf:40, timetable.dlf:30-31 (`length`, `speed`) | `"9.4"^^<https://dolfin.dev/unit/km>`, `dq:dimension` check |
| `list of` | network/network.dlf:39 | `rdfs:range rdf:List`; not filled, see limitation A |
| `inverse of` | network/network.dlf:46-47 | `owl:inverseOf network:serves` |
| `symmetric` + `sub` | network/network.dlf:50-52 | `owl:SymmetricProperty`, `rdfs:subPropertyOf network:reachable_from` |
| `transitive` | network/network.dlf:55-56 | `owl:TransitiveProperty` |
| Closed sets with fixed fields | timetable/timetable.dlf:28-38 (`VehicleType`) | `VehicleType_CITADIS_302 timetable:capacity 200` … |
| Duration bounds | timetable/timetable.dlf:49 | `sh:minInclusive "PT0S"^^xsd:duration ; sh:maxInclusive "PT5M"` |
| Cross-package check | timetable/timetable.dlf:53-54 | `sh:sparql` over `net:serves` (`PassingTime: condition not met`) |
| Inferred concept + check | timetable/timetable.dlf:65-70 (`LowFloorJourney`) | `sh:SPARQLRule` (membership) + `sh:sparql` |
| `equivalent to` with `now()` | timetable/timetable.dlf:90-96 | `FILTER(?from <= NOW())`, `NOT EXISTS` for `none until` |
| Rules on inferred classes | timetable/timetable.dlf:105, 113 | N3 rules |
| Counting rule | timetable/timetable.dlf:124-127 (`at least 2 ?l:`) | `log:collectAllIn` + `list:length` |
| XML mapping (XPath) | timetable/mappings.dlf:11, 37 | 60 rows → 108 facts |
| `case` values | timetable/mappings.dlf:22, 27, 49, 66 | enum members, `xsd:time`, `xsd:duration` literals |
| Inverse query pattern | timetable/queries.dlf:8, 18 (`is net:serves of ?_line`) | `?_line net:serves ?_stop` |
| `group by` + `count distinct`, two `order`s | timetable/queries.dlf:15-25 | `GROUP BY`, `COUNT(DISTINCT …)`, `ORDER BY DESC(?lines) ASC(?stop)` |
| First per group | timetable/queries.dlf:29-40 (`min`) | `MIN(?departure)` per line |
| Query on an inferred class at `now` | timetable/queries.dlf:43 | plain `SELECT` over the materialized data |
| Aggregation per row | timetable/queries.dlf:53-57 (`average`) | `AVG` sub-select grouped by `?line` |

## Imports, locally

There is no registry yet: an import resolves through a **lock dir** next to the importer,
`timetable/.dolfin/imports/https___www.dolfin.fr_showcase_city-transit_network-2.1.0/`, in the layout
Agrafe exports (`rust/cli-imports-todos.md`, P0):

| File | Made by |
|---|---|
| `turtle.ttl` | `radeau build network --no-comments` |
| `interface.json` | `radeau glossary network --json` (keys sorted) |
| `closure.ttl` | empty: `network` imports nothing |
| `lock.json` | `relock.sh`: IRI, version, `artifact_hash` (`glossary_ir::locks::artifact_hash`) |

`relock.sh` runs these, since radeau has no `imports fetch` yet. After any change to `network/`, from
`rust/`:

```sh
cargo build -p radeau -p radeau-glossary
RADEAU=target/debug/radeau examples/showcase/city-transit/relock.sh
cargo run -q -p radeau -- check examples/showcase/city-transit/network
cargo run -q -p radeau -- check examples/showcase/city-transit/timetable
cargo run -q -p radeau -- build examples/showcase/city-transit/timetable -o /tmp/timetable.ttl
cargo test -p radeau --test showcase_examples
```

`radeau check|build|validate` read the lock (`radeau::imports::load_package_locked`), check `net:` names
against `interface.json`, and refer to them by IRI. The importer's Turtle holds only the timetable: the
stops and lines stay in `turtle.ttl`, which a deployment loads next to it. The showcase harness does the
same, and adds the lock's `turtle.ttl` and `closure.ttl` to the data of `validate` and the queries.

A wrong imported name: `has stop: one net:Stopp` passes `radeau check` (bug B below) and fails
`radeau build` with
`Error: Code generation error: Unresolved type reference: https://www.dolfin.fr/showcase/city-transit/network/network#Stopp`.

### Bump: network 2.2.0, timetable still pins 2.1.0

Tried on a copy, with `version "2.2.0"` in `network/package.dlf`:

- Without relocking, nothing changes. The lock is a frozen copy of 2.1.0: `radeau check` on
  `timetable` is clean, and the timetable keeps seeing the 2.1.0 network, including after later network
  edits.
- After `relock.sh` (lock dir `…network-2.2.0`), `radeau check timetable` exits 1:

  ```text
  warning: import <https://www.dolfin.fr/showcase/city-transit/network>: manifest requests version 2.1.0, but the lock is for 2.2.0; export the import lock from Agrafe into .dolfin/imports/
  Error: Package error: Unresolved prefix 'fr.dolfin.showcase.city_transit.network.network' in file 'timetable/queries.dlf'
  ```

  The lock is dropped and every `net` prefix fails. The fix is to bump the `import` line to `"2.2.0"`.
  Versions are compared as exact strings: there are no version ranges.

## XML mapping walkthrough

Journey `SJ-T3-01` in `timetable/data/timetable.xml` (two of its four passing times shown):

```xml
<ServiceJourney id="SJ-T3-01">
  <LineRef ref="T3"/>
  <VehicleTypeRef ref="CITADIS_302"/>
  <DayTypeRef ref="WEEKDAY"/>
  <passingTimes>
    <TimetabledPassingTime id="SJ-T3-01-1">
      <ServiceJourneyRef ref="SJ-T3-01"/>
      <StopPointRef ref="MUS"/>
      <DepartureTime>06:20:00</DepartureTime>
    </TimetabledPassingTime>
    <TimetabledPassingTime id="SJ-T3-01-2">
      <ServiceJourneyRef ref="SJ-T3-01"/>
      <StopPointRef ref="HDV"/>
      <DepartureTime>06:30:00</DepartureTime>
      <WaitingTime>PT1M</WaitingTime>
    </TimetabledPassingTime>
    …
```

1. The first mapping (`for each "//ServiceJourney"`) makes one row of it: `?journey` = `SJ-T3-01`,
   `?line` = `T3`. `tt:{?journey}` mints the subject in the timetable namespace, and `net:{?line}`
   builds the network's IRI for line T3: a stop or line code is the network fact's name. `case` turns
   `CITADIS_302` and `WEEKDAY` into the enum members.
2. The second mapping (`for each "//TimetabledPassingTime"`) makes one row per passing time. The journey
   comes from the passing time's own `ServiceJourneyRef`, and the second template adds
   `passing_times` to the journey. `case` turns `06:30:00` into `time(06:30)` and `PT1M` into
   `duration(1min)`. `SJ-T3-01-1` has no `WaitingTime`, so the optional `dwell` is dropped for that row.

`radeau build examples/showcase/city-transit/timetable` writes (excerpt, as output):

```turtle
tt:SJ-T3-01 rdf:type owl:NamedIndividual
  , timetable:ServiceJourney
  ; rdfs:isDefinedBy <https://www.dolfin.fr/showcase/city-transit/timetable/mappings>
  .
tt:SJ-T3-01 timetable:journey_id "SJ-T3-01" .
tt:SJ-T3-01 timetable:line net:T3 .
tt:SJ-T3-01 timetable:vehicle timetable:VehicleType_CITADIS_302 .
tt:SJ-T3-01 timetable:day_type timetable:DayType_WEEKDAY .

tt:SJ-T3-01-2 rdf:type owl:NamedIndividual
  , timetable:PassingTime
  ; rdfs:isDefinedBy <https://www.dolfin.fr/showcase/city-transit/timetable/mappings>
  .
tt:SJ-T3-01-2 timetable:journey tt:SJ-T3-01 .
tt:SJ-T3-01-2 timetable:stop net:HDV .
tt:SJ-T3-01-2 timetable:departure "06:30:00"^^xsd:time .
tt:SJ-T3-01-2 timetable:dwell "PT1M"^^xsd:duration .

# Fact: tt:SJ-T3-01
tt:SJ-T3-01 rdf:type owl:NamedIndividual
  , timetable:ServiceJourney
  ; rdfs:isDefinedBy <https://www.dolfin.fr/showcase/city-transit/timetable/mappings>
  .
tt:SJ-T3-01 timetable:passing_times tt:SJ-T3-01-2 .
```

with `@prefix net: <https://www.dolfin.fr/showcase/city-transit/network/network#>` and
`@prefix tt: <https://www.dolfin.fr/showcase/city-transit/timetable/timetable#>`. `net:T3` and `net:HDV`
are only referenced: no `net:` subject appears in the timetable's Turtle. The passing time calls at Hôtel
de Ville, so at `now` the rules make `SJ-T3-01` a `DisruptedJourney`.

## Validation and queries

`timetable/validate/`:

- `ok/extra_journey.ttl`: an evening T1 short working.
- `bad/stop_not_on_line.ttl`: a T1 journey timed at Hôtel de Ville, which T1 does not serve (the
  cross-package check).
- `bad/dwell_too_long.ttl`: a 7-minute wait.
- `bad/journey_without_line.ttl`: no `line`.
- `bad/low_floor_inaccessible_stop.ttl`: bus 10 run with a low-floor bus, calling at Opéra.

`network/validate/bad/latitude_out_of_range.ttl` holds the latitude case (145.76°): it is a network
shape, and the timetable's `validate` does not run the import's shapes (limitation G).

`timetable/queries/expected/` was worked out by hand from the network facts and the XML, then compared
with the harness output (no difference):

- `lines_at_stop`: B11, T2, T3 at Hôtel de Ville.
- `interchanges`: Gare Centrale and Hôtel de Ville (3 lines), République and Université (2).
- `first_departures`: T1 06:00, T2 06:10, T3 06:20, B11 06:40, B10 06:50 (weekday journeys only).
- `disrupted_journeys_now`: the seven journeys timed at Hôtel de Ville (T2, T3, B11). Without the
  `validate/now` pin, the default `now` (2026-06-15) is before D-0412, and the query is empty.
- `capacity_per_line`: B10 95, B11 150, T1 300, T2 250 (one CITADIS 302, one 402), T3 200.

## Limitations

The letters refer to the "city-transit showcase" section of `rust/BUGS.md`, except where another section
is named.

- **`list of` in facts** (BUGS mountain-ultra A). `Line.stops` is declared but not filled: a list value
  in a fact becomes one triple per stop and fails `sh:maxCount 1`. `serves` lists each line's stops in
  running order instead.
- **OWL characteristics are not reasoned on** (BUGS mountain-ultra F). `symmetric`, `transitive` and
  `inverse of` compile to OWL only: the harness materializes RDFS, so no reverse walkway and no
  `served_by` triple is inferred. Queries therefore use `is net:serves of ?line`, not `net:served_by`.
- **A.** Imported names are written `net:Stop`. The dotted `net.Stop` builds, but `radeau check`
  reports `error[S001]: type `net.Stop` is not declared`.
- **B.** `radeau check` accepts an undefined imported name (`net:Stopp`). Only `radeau build` fails.
- **C.** An XML mapping has one `for each`, and XPath has no `..`, so passing times cannot be read
  nested inside their journey. The export repeats a `ServiceJourneyRef` in every
  `TimetabledPassingTime` (real NeTEx does not), and a second mapping iterates the passing times.
- **D.** There is no `as time` (or `as duration`) cast. `case` tables turn the 16 departure times and
  the 2 waiting times of the export into literals, so a new time in the XML needs a new `case` arm (an
  unmatched `departure` skips its row).
- **E.** `rule interchange` was to match two lines `?l1`, `?l2` with `?l2 net:code [ != ?c1 ]`. That
  compiles to `math:notEqualTo` and never matches string codes. The rule counts lines with
  `at least 2 ?l:` instead.
- **F.** A condition only walks forward from its focus node (no `^p`, no `is p of`), so the
  "stop on the journey's line" check cannot start from the journey. `PassingTime` has a `journey` back
  link (written by the mapping), and the check sits on `PassingTime`.
- **G.** `radeau validate` on the importer loads neither the import's Turtle nor its shapes. The harness
  passes the lock's `turtle.ttl` as `--data`, and the latitude bound is only checked in `network`.
- **H.** An unqualified field in a condition is not checked: `stop [ accessible [ = true ] ]` silently
  meant `timetable:accessible`, and the check never fired. It has to be written `net:accessible`.
- **I.** `return` order does not set the column order of a grouped query: `interchanges` returns
  `stop  lines`, and `first_departures` returns `line  first`.
- **J.** `radeau fmt` refused a prefixed type in `has` (`net:Line`) and a negative bound
  (`[ >= -90 ]`). Both were fixed in passing. It still refuses a comment group that is separated by a
  blank line from a fact with its own doc comment, so the line descriptions sit in one comment above
  the lines.
- **K.** A negative field bound is dropped: `[ >= -90, <= 90 ]` emits only `sh:maxInclusive 90`, so a
  latitude of −145 conforms. A negative number in a fact (`lat -12.5`) is a parse error, so the
  network could not have a stop west of Greenwich or south of the equator.
- `now()` is not allowed in a rule `match:` (BUGS seed-cooperative), so "active" is two
  `equivalent to` concepts, `OpenDisruption` and `CurrentDisruption`, with one rule each. A single
  `[ from [ <= now() ], until [ >= now() ] ]` would also work (`all` is vacuously true without `until`),
  but `radeau check` warns `L/semantic/vacuous-all` about it.
- The lint asks for camelCase property names (`served_by` → `servedBy`). The showcase keeps the
  snake_case names of the brief, so `radeau check` on `network` prints three warnings.
