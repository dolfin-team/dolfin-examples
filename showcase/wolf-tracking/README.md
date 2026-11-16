# Wolf tracking

The research team of the Parc des Hautes Vallées (fictional, Mercantour-like, invented
coordinates in 44.0–44.4 N, 6.8–7.4 E) follows four GPS-collared wolves from two packs:
F23 and M17 of the Nord-Vallon pack, M31 and F08 of the Crête Blanche pack. The team uses
field names (F23 is the 23rd female collared), not human names.

- Every 2 hours, a collar uploads a fix with latitude, longitude, elevation, a UTC timestamp,
  the number of satellites and the HDOP (horizontal dilution of precision: lower is better).
  The export is `data/collars.csv`.
- Rangers walk transects with a handheld GPS. Its GPX 1.1 export,
  `data/ranger-2026-07-12.gpx`, holds the ranger's track and one waypoint per sighting
  (scat, tracks, a howl, a visual).

The team wants to know:

- which wolves enter the summer sheep pastures (alpages) at night, during the grazing season;
- which fixes are too imprecise to trust;
- each wolf's elevation range;
- per-pack activity;
- which ranger sightings lie close in space and time to a collar fix.

`generate_fixes.py` (stdlib only, seeded) writes both data files: 4 wolves × 5 days
(8–12 July 2026) × 12 fixes, plus one extra fix and one duplicate upload (242 rows), and
37 track points with 5 waypoints. The fixes are random walks in each pack's home range,
kept out of the alpages and villages. Every alpage visit is scripted:

| Wolf | Zone | Night fixes | Counted as raids | Why |
|---|---|---|---|---|
| F23 | ALP_CABANE | 6, on 4 nights | 5 → **AlpageRaider** | the 6th has HDOP 6.8 (`UnreliableFix`) |
| M17 | ALP_CABANE | 2, on 1 night | 2 | under the threshold of 3 |
| M31 | ALP_LAUSES | 3, on 1 night | 0 | the Lauses season opens on 15 July |

F23 is also in the Cabane at 04:00Z on 12 July. That is 06:00 local, which is day, so it is not
a night fix. Its pack, Nord-Vallon, is the one `ProblemPack`.

## Map

```text
 44.40 N +---------------------------------------------------------------+
         |                     Saint-Ours (VILLAGE)                      |
         |                       [ ]  44.335-44.345 / 6.990-7.005        |
         |        Nord-Vallon range      Alpage de la Cabane (ALPAGE)    |
         |          F23  M17  ~~~~>       [###]  44.270-44.285            |
         |        (44.30, 7.00)           F23: 4 nights, M17: 1 night     |
         |  +-----------------+                  7.040-7.060              |
         |  | Réserve du      |                                           |
         |  | Vallon Sombre   |  CORE_RESERVE 44.180-44.240               |
         |  +-----------------+               6.950-7.020                 |
         |                         Alpage des Lauses (ALPAGE) [##]        |
         |                         44.155-44.165 / 7.170-7.185            |
         |                         M31, 9-10 July (season from 15 July)   |
         |                              Crête Blanche range  M31  F08     |
         |                              (44.13, 7.21)   ranger, 12 July   |
         |                                         Le Pra (VILLAGE) [ ]   |
         |                                         44.100-44.108          |
 44.00 N +---------------------------------------------------------------+
       6.80 E                                                        7.40 E
```

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| Latitude / longitude with range constraints | tracking.dlf:44, rangers.dlf:30, zones.dlf:16 | `sh:maxInclusive "90"^^xsd:integer` (the `-90` bound is dropped: limitations) |
| Elevation as a quantity | tracking.dlf:46, mappings.dlf:37 | `rdfs:range quantitykind:Length`, an `a Length quantity (dimension L1)` node shape; `"1481"^^<https://dolfin.dev/unit/m>` |
| `one of:` with key fields | tracking.dlf:14 (`Pack`) | `owl:oneOf`, `owl:hasKey ( tracking:code )` |
| Two-field `key:` block (collar + at) | tracking.dlf:37 | `owl:hasKey`; retox and SHACL-AF `owl:sameAs` rules (the duplicate upload) |
| `check` across an object | tracking.dlf:55 | `sh:sparql` (`Fix: condition not met`) |
| `equivalent to` + `check` | tracking.dlf:60 (`WeakFix`) | `sh:sparql` (`WeakFix: condition not met`) |
| Variable-to-variable comparisons (bounding box) | tracking.dlf:83 (`in_zone`) | `?f tracking:lat ?_v4 . ?_v4 math:notLessThan ?lat_lo . ?_v4 math:notGreaterThan ?lat_hi .` |
| `none ?f:` in a rule, date comparisons | tracking.dlf:112 (`raid_fix`) | `?_scope log:notIncludes { ?f a tracking:UnreliableFix . }` |
| `count` in a rule | tracking.dlf:125 (`alpage_raider`) | `( ?f { … } ?_v10 ) log:collectAllIn ?_scope . ?_v10 list:length ?n .` |
| `count distinct` over a class derived by an aggregate | tracking.dlf:135 (`active_pack`) | a later retox stratum than `alpage_raider` |
| `min` / `max` in a rule | tracking.dlf:145 (`elevation_range`) | `( ?e { … } ?_v12 ) log:collectAllIn ?_scope . ?_v12 math:min ?low .` |
| Space + time correlation | rangers.dlf:54 (`confirmed_sighting`) | six `math:` comparisons on the sighting's precomputed box and window |
| `@timezone Europe/Paris` | rangers.dlf:1, 77 | `"2026-07-12T07:00:00+02:00"^^xsd:dateTime` |
| CSV mapping, casts, `slug()` | mappings.dlf:16 | `trk:fix_U00001 tracking:collar trk:phv_0423 .`, typed literals |
| XML mapping of a namespaced GPX | mappings.dlf:44, 60 | one `RangerPosition` per `trkpt`, one `Sighting` per `wpt` |
| `case` table | mappings.dlf:77 | `rangers:kind rangers:SightingKind_SCAT` |
| `order` + string-range filter + `limit` | queries.dlf:71 (`ranger_track`) | `FILTER (?at >= "2026-07-12T")`, `ORDER BY ASC(?at) LIMIT 20` |
| `group by` with 3 counts | queries.dlf:29 (`fixes_per_wolf`) | `COUNT`, `COUNT(DISTINCT …)` |
| `none:` in a query | queries.dlf:57 (`unconfirmed_sightings`) | `FILTER NOT EXISTS` |
| HAVING-style filter | queries.dlf:91 (`pack_activity`) | `HAVING (COUNT(DISTINCT ?_f) >= 1)` |

## Modelling positions without a geo type

- A position is two `float`s, `lat` and `lon`, with range constraints.
- A zone is a bounding box: `min_lat`, `max_lat`, `min_lon`, `max_lon`. "Inside" is four
  comparisons between variables (`in_zone`).
- "Close to" a sighting is a box of ±0.005° (about 500 m in latitude, 400 m in longitude here)
  and a window of ±120 min. A rule cannot add a number to a stored value, and a mapping cannot
  compute either. The box and the window are therefore written by the GPS export, in a
  `<phv:search>` element of the waypoint's `<extensions>` (GPX's extension point), and mapped
  like any other value. The window is in Unix minutes (`t_min`), because times are text
  (see the limitations).

S1, S3 and S4 are confirmed by F08, which left them 60–100 min before the ranger found them.
S2 and S5 lie on the ranger's walk where no wolf was: `unconfirmed_sightings`.

## GPX mapping walkthrough

GPX 1.1 puts every element in the default namespace `http://www.topografix.com/GPX/1/1`.
`mappings.dlf` declares it as a prefix and uses prefixed paths:

```dolfin
prefix <http://www.topografix.com/GPX/1/1> as gpx

mapping from <package://data/ranger-2026-07-12.gpx> as XPath
  for each "/gpx:gpx/gpx:trk/gpx:trkseg/gpx:trkpt"
  map:
    "@lat"     as ?lat
    "@lon"     as ?lon
    "gpx:ele"  as ?ele
    "gpx:time" as ?at
  to:
    fact rng:pos_r_lb_{slug(?at)} a rangers.RangerPosition
      rangers.by rng:R_LB
      rangers.at {?at}
      rangers.lat {?lat} as float
      rangers.lon {?lon} as float
      rangers.elevation {?ele} as quantity(m)
```

An unprefixed path (`/gpx/trk/…`) would match elements in any namespace, so it would not test
the namespace. Attributes (`@lat`) take no default namespace and stay unprefixed. The first
track point:

```xml
      <trkpt lat="44.10918" lon="7.17261">
        <ele>1481</ele>
        <time>2026-07-12T05:00:00Z</time>
      </trkpt>
```

The output of `radeau build examples/showcase/wolf-tracking`:

```turtle
# Fact: rng:pos_r_lb_2026_07_12t05_00_00z
rng:pos_r_lb_2026_07_12t05_00_00z rdf:type owl:NamedIndividual
  , rangers:RangerPosition
  ; rdfs:isDefinedBy <https://www.dolfin.fr/showcase/wolf-tracking/mappings>
  .
rng:pos_r_lb_2026_07_12t05_00_00z rangers:by rng:R_LB .
rng:pos_r_lb_2026_07_12t05_00_00z rangers:at "2026-07-12T05:00:00Z" .
rng:pos_r_lb_2026_07_12t05_00_00z rangers:lat "44.10918"^^xsd:float .
rng:pos_r_lb_2026_07_12t05_00_00z rangers:lon "7.17261"^^xsd:float .
rng:pos_r_lb_2026_07_12t05_00_00z rangers:elevation "1481"^^<https://dolfin.dev/unit/m> .
```

A GPX file is one ranger's walk, and the mapping language has no nested `for each`, so the ranger
is a constant (`rng:R_LB`) rather than read from `<trk>`.

## The time zone

The collars and the GPX write UTC. "Night" is defined in local time: before 06:00 or from 21:00
in Europe/Paris. In July that is CEST, UTC+2, so the 2-hour schedule (00, 02, … 22 UTC) gives
night fixes at 20, 22, 00 and 02 UTC. Reading the UTC hour directly would be wrong twice per
day:

| UTC | Local | Night? | A UTC reading would say |
|---|---|---|---|
| 20:00Z | 22:00 | yes (M17, 10 July, in the Cabane) | day |
| 21:30Z | 23:30 | yes (F23's extra fix, 9 July) | night (by luck) |
| 04:00Z | 06:00 | no (F23, 12 July, in the Cabane) | night |

Rules cannot extract an hour from a `date_time`, and mappings cannot cast one, so
`generate_fixes.py` computes `is_night` with `zoneinfo("Europe/Paris")` and the rule `night_fix`
reads it. It is correct in winter (UTC+1) too, because the generator converts each instant instead
of applying a fixed offset. The data covers July only.

`@timezone Europe/Paris` (rangers.dlf:1) applies to times written in Dolfin.
`date_time(July 12th 2026, 07:00)` in the `Transect` fact becomes
`"2026-07-12T07:00:00+02:00"^^xsd:dateTime`, which is the same instant as the first GPX point,
`05:00:00Z`.

## Why no GeoSPARQL

Dolfin has no geometry type, and SPARQL 1.1 has no trigonometry, so this package compares
coordinates as plain numbers inside boxes. Doing it properly would need a real geo feature:

- **Distance**: haversine needs `sin`, `cos` and `asin`, or a `geof:distance` function. The ±0.005°
  box is about 500 m north–south but only 400 m east–west at 44° N.
- **Polygons**: a real alpage boundary is not a rectangle.
- **WKT literals**: `"POINT(7.05 44.27)"^^geo:wktLiteral` as a field type, with a mapping cast from
  lat/lon.
- **Spatial relations**: `geof:sfWithin` and `geof:sfIntersects` in rules and queries, which needs
  a store with a spatial index.

## Commands

From `rust/`:

```sh
python3 examples/showcase/wolf-tracking/generate_fixes.py                   # data/
python3 examples/showcase/wolf-tracking/generate_fixes.py --print-expected  # queries/expected/
cargo run -q -p radeau -- check examples/showcase/wolf-tracking
cargo run -q -p radeau -- build examples/showcase/wolf-tracking -o /tmp/wolves.ttl
cargo run -q -p radeau -- build examples/showcase/wolf-tracking --emit n3-rules -o /tmp/wolves.n3
cargo run -q -p radeau -- validate examples/showcase/wolf-tracking --now 2026-07-13T12:00:00Z \
  --data examples/showcase/wolf-tracking/validate/bad/latitude_out_of_range.ttl
cargo test -p radeau --test showcase_examples
cargo test -p dolfin-lint --test fmt_examples
```

`validate/ok/extra_fix.ttl` is a late F23 upload. `validate/bad/` has one violation per file: a
latitude of 95.2, an elevation in seconds, a fix before F08's collaring date, a negative HDOP, a
fix without a collar, and a 3-satellite fix with an HDOP of 1.1 (`WeakFix`). The `.expect`
substrings are copied from `radeau validate`'s stderr. `queries/expected/` comes from
`generate_fixes.py --print-expected`, which replays the rules in Python. The alpage counts in the
table above were checked by hand against the script.

## Limitations

The letters refer to `rust/BUGS.md`, under "wolf-tracking showcase" unless another showcase is
named.

- **Five days, not thirty (B).** The `Fix` key (collar + at) joins every pair of fixes of a collar
  before it compares `at`. At 1442 fixes the harness took 1127 s for retox and 27 min per
  `radeau validate`, so the generator writes 5 days. The key stays and its `owl:sameAs` rule
  runs. Queries act on its `owl:sameAs`, rules do not (mountain-ultra C): `fixes_per_wolf` counts F08's
  duplicate upload once, 60 uploads and 60 fixes.
- **Aggregate rules conclude classes only (A).** retox now accepts a `count` rule that concludes
  a property, or a subclass of a keyed concept (fixed 2026-11-14), but the showcase was written
  before: `RaidFix`, `AlpageRaider` and `ProblemPack` are not subclasses of `Fix`, `Wolf` and
  `Pack`, and the raid count is in the `alpage_raiders` query instead of a `raid_count` field.
- **Times are text** (city-transit D: no `as date_time` cast). `at` is a `string` (ISO 8601 UTC).
  Windows use `t_min` (Unix minutes), the day is a separate `date` column, and `is_night` is
  precomputed. A `date` never compares with a `date_time` (hospital-pharmacy D) anyway, so the
  grazing season and the collaring check use `day`.
- **No bound on `elevation`** (hospital-pharmacy A: any bound on a quantity rejects every value).
- **`lat [ >= -90 ]` emits no `sh:minInclusive`** (city-transit K). Only the upper bounds are
  checked, and the park is in the north-east quadrant.
- **No nested `for each`** (city-transit C): the ranger is a constant in the GPX mappings.
- **`?lat [ >= ?lo ]` on its own line is taken for an aggregate (C)**: the rules write
  `?f lat [ >= ?lo, <= ?hi ]`.
- **No text between two holes in a subject (D)**: the fixes are named after the CSV's `upload_id`.
