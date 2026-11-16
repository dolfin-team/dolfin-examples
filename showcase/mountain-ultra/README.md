# Mountain ultra-trail

The Ultra des Trois Cols (fictional race, real places) is a 78 km loop from Bourg-Saint-Maurice
with 4800 m of positive gain, run on Saturday 11 July 2026. The start is at 05:00 local time. The
course climbs the Col du Petit-Saint-Bernard, crosses into Italy at La Thuile, comes back over the
Col de la Seigne, passes the Refuge des Mottets and Les Chapieux, and climbs the Cormet de Roselend
before the descent to the finish. Each of the eight checkpoints (CP1 … CP7, FINISH) has a distance
from the start, an altitude, a cumulative D+ and a cutoff in Europe/Paris local time.

Runners have a bib, an age category, a birthdate and a mandatory gear list. Timing mats record one
`date_time` per runner per checkpoint. The chips record UTC and the aid-station volunteers record
local time. The officials want to know who was timed out at a cutoff, who finished, each runner's
average speed and the ranking overall and by category.

Data: 30 runners. Bibs 101-120 finish, 121-126 stop at an aid station, 127-128 are timed out at a
cutoff, and 129-130 did not start. Emma (112) has no survival blanket and Marta (124) has no water.
Three cutoff edge cases are commented in `race.dlf`:

1. **Monique (120) at the Col de la Seigne at 13:30 UTC, which is exactly the 15:30 local cutoff.**
   Cutoffs are inclusive. The rule uses `cutoff < at` and the check uses `cutoff >= at`, so she is
   neither flagged nor in violation, and she finishes.
2. **Rémi (127) at Les Chapieux at 15:32 UTC, which is 17:32 local, two minutes after the 17:30
   cutoff.** He gets `DNFCutoff`.
3. **Julie (128) at the Cormet de Roselend at 18:40 UTC.** Read as local time, that beats the 20:00
   cutoff. It is 20:40 in Europe/Paris, so she is 40 minutes late and gets `DNFCutoff`. The
   comparison is between instants: `"2026-07-11T18:40:00+00:00"` is after
   `"2026-07-11T20:00:00+02:00"`.

A deliberate duplicate is also in the facts. The La Thuile volunteers wrote Hugo (105) on their paper
sheet in local time (`p105_cp3_sheet`, 08:50 +02:00), at the same instant as the chip record. The
two-field `Passage` key (runner + checkpoint) infers `owl:sameAs` between the two records.

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| `@timezone Europe/Paris` | course.dlf:1 | cutoffs `"2026-07-11T15:30:00+02:00"^^xsd:dateTime` (CEST) |
| Inline `UTC` / `+02:00` offsets | race.dlf:1222, 614 | `"…T13:30:00+00:00"`, `"…T08:50:00+02:00"` |
| Dimension-typed fields (`length`, `speed`) | race.dlf:14-19, 68 | `rdfs:range quantitykind:Length`; `sh:node … dq:dimension "L1"` (wrong unit: S008 / violation) |
| Unit conversion with `as` | course.dlf:29, 31, 49, 84, 86 | `"21.999732480000002"^^<…/unit/km>`, `"2516.1240000000003"^^<…/unit/m>` |
| Unit arithmetic `78 km / 585 min as km/h` | race.dlf:167 and every finisher | `"8"^^<https://dolfin.dev/unit/km.h-1>` |
| `list of Checkpoint` | race.dlf:33 | `rdfs:range rdf:List`; `sh:node [ sh:property [ sh:path ( [ sh:zeroOrMorePath rdf:rest ] rdf:first ) … ] ]` |
| `set of GearItem` | race.dlf:61 | plain multi-valued object property |
| `inverse of` / `transitive` | race.dlf:24-27 | `owl:inverseOf race:previous`, `owl:TransitiveProperty` |
| `key:` block (runner + checkpoint) | race.dlf:89 | `owl:hasKey ( race:runner race:checkpoint )`; retox `owl:sameAs` rule |
| Class expression `with gear: = …` | race.dlf:80 (`FullyEquipped`) | `owl:intersectionOf ( race:Runner [ owl:hasValue race:GearItem_HEADLAMP ] … )` |
| Inverse restriction `with ^runner:` + nested `with` | race.dlf:105 (`Finisher`) | `owl:onProperty [ owl:inverseOf race:runner ] ; owl:someValuesFrom [ … owl:hasValue course:finish ]` |
| Derived field from `now()` | race.dlf:63 (`age`) | `sh:SPARQLFunction` |
| `check` with `$age` | race.dlf:76 (category vs age) | `sh:sparql` (`Runner: condition not met`) |
| `check` comparing two `date_time`s | race.dlf:97 (`RankedPassage`) | `sh:sparql` (`RankedPassage: condition not met`) |
| Closed sets with fixed fields | race.dlf:36, 45 | `owl:oneOf`; `Category_M1_H` with `min_age "P40Y"` |
| Rule, variable-to-variable `date_time` comparison | race.dlf:116 (`dnf_cutoff`) | N3 `?_v2 math:lessThan ?t` |
| Rule `none` over three triples | race.dlf:132 (`missing_gear`) | `log:notIncludes { … }` |
| Transitive chain as rules | race.dlf:144, 150 | N3 rules filling `after` |
| `order asc` + `limit` | queries.dlf:5 | `ORDER BY ASC(?finish_time) LIMIT 10` |
| `group by` + `count` / `average` | queries.dlf:18, 30 | `GROUP BY`, `COUNT`, `AVG` |
| `none:` with a nested pattern | queries.dlf:42 | `FILTER NOT EXISTS { ?_q runner ?r ; checkpoint [ after ?cp ] }` |

## Units in action

The facts convert at parse time, and the Turtle holds the converted value in the target unit. These
lines are copied from `radeau build examples/showcase/mountain-ultra`:

```turtle
course:cp2 race:distance_from_start "21.999732480000002"^^<https://dolfin.dev/unit/km> .   # quantity(13.67 mi as km)
course:cp4 race:altitude "2516.1240000000003"^^<https://dolfin.dev/unit/m> .              # quantity(8255 ft as m)
course:cp2 race:cumulative_gain "1500"^^<https://dolfin.dev/unit/m> .                     # quantity(1.5 km as m)
race:r101 race:avg_speed "8"^^<https://dolfin.dev/unit/km.h-1> .                          # quantity(78 km / 585 min as km/h)
race:r104 race:avg_speed "6.75"^^<https://dolfin.dev/unit/km.h-1> .                       # quantity(78 km / 41600 s as km/h)
```

13.67 mi × 1.609344 is exactly 21.99973248 km, and 8255 ft × 0.3048 is exactly 2516.124 m. The
trailing digits are f64 rounding, and they are kept in the lexical form. The unit definitions
(`dq:coefficient`, `dq:dimension "L1.T-1"`) are emitted at the end of the file, so rule comparisons
between units stay unit-aware.

## Commands

From `rust/`:

```sh
cargo run -q -p radeau -- check examples/showcase/mountain-ultra
cargo run -q -p radeau -- build examples/showcase/mountain-ultra -o /tmp/ultra.ttl
cargo run -q -p radeau -- build examples/showcase/mountain-ultra --emit shacl -o /tmp/ultra-shacl.ttl
cargo run -q -p radeau -- validate examples/showcase/mountain-ultra --now 2026-07-12T12:00:00Z \
  --data examples/showcase/mountain-ultra/validate/bad/utc_late_after_conversion.ttl
cargo run -q -p radeau -- fmt --check examples/showcase/mountain-ultra
cargo test -p radeau --test showcase_examples
cargo test -p dolfin-lint --test fmt_examples
```

`validate/ok/` contains three conforming files:

- a volunteer's late paper entry;
- edge case 1 submitted for the ranking (`RankedPassage` exactly at the cutoff);
- the course as a real `rdf:List`.

`validate/bad/` contains one violation per file:

- a passage one minute after the cutoff;
- edge case 3 submitted for the ranking;
- a distance in seconds;
- a passage without a checkpoint;
- a master 2 runner who is 41.

`queries/expected/` was computed by hand from the facts (finish times sorted; counts and averages per
category, the averages in single precision because `float` is `xsd:float`).

## Limitations hit

The letters refer to the entries under "mountain-ultra showcase" in `rust/BUGS.md`, or under
"hospital-pharmacy showcase" when marked HP.

- **Rules have no arithmetic or aggregates.** The finish time (`duration`) and the average speed
  (`quantity(78 km / … as km/h)`) are therefore precomputed facts, not derived from the passages.
- **A.** The checkpoint list is not asserted in the facts. A `list of` value in a fact becomes plain
  triples, which fail `sh:maxCount 1`. `validate/ok/course_as_rdf_list.ttl` supplies the
  `rdf:List`. The course order used by the queries comes from `next` / `after`.
- **B.** `average` over the quantity `avg_speed` is unbound. `average_speed_by_category` averages
  `avg_speed_kmh`, a plain `float` that holds the same value.
- **C.** The two-field `Passage` key makes the harness's materialization take ~48 s in a debug build
  (5.6 s without it). Queries act on the inferred `owl:sameAs`: `merged_passages` returns both time
  stamps under the canonical IRI `p105_cp3`. Rules do not: they match each record. `owl:sameAs`
  itself cannot be queried from Dolfin.
- **D.** `checkpoint_profile` orders by distance lexically. The order is right only because every
  distance has two integer digits.
- **E.** Rule `none` needs a variable. `missing_gear` is written `none ?r:`.
- **F.** `transitive`, `inverse of`, `FullyEquipped` and `Finisher` are OWL only, and retox does not
  reason on them. The rules `next_is_after`, `passed_after` and `finisher` provide what the queries
  need. `GearPenalty` is the `none` rule, not the complement of `FullyEquipped`.
- **HP A.** `altitude` has no `[ >= 0 ]`, because a bound on a quantity field rejects every value.
  `altitude_negative.ttl` therefore sits in `validate/known-bug/`. It conforms today; move it to
  `bad/` once HP A is fixed.
- **HP C.** The category check uses `$age` (`[ category [ min_age [ <= $age ], max_age [ > $age ] ] ]`).
  The property form `age [ … ]` reads a stored triple.
- The materialized store returns UTC times as `Z` (`2026-07-11T06:50:00Z`), although the built
  Turtle has `+00:00`.
