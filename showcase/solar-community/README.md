# Citizen solar energy community: Soleil du Diois

Soleil du Diois (fictional) is a citizen energy community in a Drôme valley. Twenty households, the village
école, a summer day-camp and a cheese dairy share the output of rooftop PV installations connected to two
low-voltage feeders, DEPART_A and DEPART_B. Each site has a smart meter that reports, every day, the energy it
imported, the energy it exported and the highest power it drew. The older meters report in **Wh**, the newer ones
in **kWh**, and the école's in **MWh**. One household's Wh meter was replaced by a kWh one in the middle of the
month.

The community wants to know:

- each site's and each feeder's monthly totals;
- which sites drew more than their contracted power;
- how much of what it imports it also exports (its self-consumption balance);
- which feeders have so many producers that they all export at once on a sunny noon;
- which installations exported nothing (a fault), and whether the école is on holiday.

The point of the example is **aggregates in rule `match:` blocks**: `sum`, `max`, `average`, `count` and
`count distinct` over energy and power quantities in mixed units, in rules stratified after a plain rule. The
same aggregates also appear in queries.

**The month is July 2026.** PV output is at its highest, so the feeders export a lot. The école closes for the
summer after Friday 3 July, so one month holds both its school days and its holiday. That gives
`low_average_school` a site that fires (the école) next to one that does not (the day-camp, open on weekdays all
summer). In January, the school would be in session all month except the first two days.

Data: 23 sites, 7 PV installations, and 682 daily readings (22 sites × 31 days; H11 has none), in
`data/readings.csv`. `generate_readings.py` wrote them once with a fixed seed, and running it again writes the same
bytes.

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| Dimension-typed fields | community.dlf:45, 47 (`energy`, `power`) | `sh:node` dimension check, `dq:dimension "L2.M1.T-2"` |
| Closed set with fixed fields and a key | community.dlf:12-18 (`Feeder`) | `owl:oneOf`, `community:Feeder_DEPART_A community:max_injection "60"^^<…/unit/kW>` |
| `has key` (14-digit PDL) | community.dlf:22 | `owl:hasKey`, SHACL key rule |
| Two-field `key:` block (site + day) | community.dlf:39-41 | `CONSTRUCT { $this owl:sameAs ?o }`, a "two values via key merge" `sh:sparql` per field |
| `property` for a computed quantity | community.dlf:73 | `owl:DatatypeProperty`, no shape (Limitations, B) |
| Plain rule, stratum 0 | community.dlf:77 (`producer`) | N3 rule, `sh:SPARQLRule` |
| `sum` in a rule, mixed units, value in `then:` | community.dlf:87 (`monthly_import_total`) | `CONSTRUCT` + grouped sub-`SELECT`, below |
| `max` in a rule, literal threshold | community.dlf:100-128 (`over_contract_*`) | `MAX(?_v1)`, then the `dq:` unfolding of `> quantity(6 kW)` |
| `count distinct` over a derived class | community.dlf:132 (`crowded_feeder`) | `OPTIONAL { SELECT … COUNT(DISTINCT ?site) }` + `COALESCE(?_c0, 0)`; N3 `log:collectAllIn` |
| `count` over an empty group is 0 | community.dlf:146 (`idle_installation`) | `COALESCE(?_c0, 0)`; no N3 (a second local variable) |
| `average` + boolean + date filter | community.dlf:159 (`low_average_school`) | `AVG(?_v1)`, `?_v9 >= "2026-07-06"^^xsd:date` inside the sub-`SELECT` |
| Unit-aware comparison in a rule | community.dlf:171, 177 (`invalid_*`) | N3 `?_v10 dq:lessThan "0"^^<…/unit/W.h>` |
| Rule → class → `minCount` violation | community.dlf:66 (`InvalidReading`) | `sh:targetClass community:InvalidReading ; sh:minCount 1` |
| Aggregate cycle (comment) | community.dlf:183-201 | `Unstratifiable negation cycle`, below |
| CSV mapping, one per unit, `where:` | readings.dlf:12, 25, 39, 53 | `"5951"^^<…/unit/W.h>`, `"4.1"^^<…/unit/h.kW>`, `"0.155"^^<…/unit/MW.h>` |
| `as boolean`, `as date`, `as quantity(kW)` | readings.dlf:21-24 | `xsd:boolean`, `xsd:date`, `"4"^^<…/unit/kW>` (the CSV says `4.0`) |
| `group by` + two `sum`s | queries.dlf:5-12 | `GROUP BY ?feeder`, `SUM(?exp)` (Limitations, hospital-pharmacy E) |
| Rule output + `order desc` + `limit` | queries.dlf:16-24 | `ORDER BY DESC(?total) LIMIT 5` |
| Per-row aggregates, no shared variable | queries.dlf:27-33 | two sub-`SELECT`s, one row |
| Inferred class + per-row `max` | queries.dlf:37-46 | `{ SELECT ?s (MAX(?p) AS ?peak) … GROUP BY ?s }` |
| `group by` + `count distinct` + `HAVING` | queries.dlf:49-54 | `HAVING (COUNT(DISTINCT ?site) >= 3)` |
| Query on an aggregate rule's class | queries.dlf:58 | plain `SELECT` over the retox-materialized store |

Units: `kW.h` is written `h.kW` in the IRIs (`"4.1"^^<https://dolfin.dev/unit/h.kW>`). The `dq:` block of
`radeau build`:

```turtle
<https://dolfin.dev/unit/MW.h> dq:coefficient 3600000000 ; dq:dimension "L2.M1.T-2" ; dq:symbol "MW.h" .
<https://dolfin.dev/unit/W.h> dq:coefficient 3600 ; dq:dimension "L2.M1.T-2" ; dq:symbol "W.h" .
<https://dolfin.dev/unit/h.kW> dq:coefficient 3600000 ; dq:dimension "L2.M1.T-2" ; dq:symbol "kW.h" .
<https://dolfin.dev/unit/kW> dq:coefficient 1000 ; dq:dimension "L2.M1.T-3" ; dq:symbol "kW" .
```

### An aggregate rule in SHACL-AF

`radeau build examples/showcase/solar-community --emit shacl` emits `monthly_import_total` as follows (copied from
the output):

```turtle
community:monthly_import_totalRule a sh:NodeShape
  ; sh:targetNode community:monthly_import_totalRule
  ; sh:rule [ a sh:SPARQLRule ; sh:order 1 ; sh:prefixes _:prefixes ; sh:construct """CONSTRUCT { ?site community:monthly_import ?total . } WHERE {
  ?site a community:Site .
  {
    SELECT ?site (IF(COUNT(DISTINCT ?_u0) = 1, STRDT(str(SUM(?_v1)), SAMPLE(?_u0)), STRDT(str(SUM((?_v1 * ?_k2))), <https://dolfin.dev/unit/kg.m2.s-2>)) AS ?total)
    WHERE {
      ?r community:site ?site .
      ?r community:imported ?e .
      BIND(datatype(?e) AS ?_u0)
      BIND(xsd:double(str(?e)) AS ?_v1)
      OPTIONAL { ?_u0 <https://dolfin.dev/quantity#coefficient> ?_k2 . }
    }
    GROUP BY ?site
  }
}""" ]
  .
```

**The unit of a sum.** When all of a site's readings have one unit, the sum keeps it: a Wh meter sums to Wh, the
école's to MWh. When the units differ, each value is multiplied by its unit's `dq:coefficient` and the sum is in the
SI unit, J, written `kg.m2.s-2`. Run by `radeau validate`, the rule gives (checked by hand against the CSV with
`awk`):

| Site | Meter | `monthly_import` | Check |
|---|---|---|---|
| H04 Foyer Daumas | Wh | `"268159"^^unit:W.h` | 31 readings, 268 159 Wh = 268.159 kWh |
| H07 Foyer Giraud | Wh, then kWh from 16 July | `"999860400"^^unit:kg.m2.s-2` | 143 609 Wh + 134.13 kWh = 277.739 kWh × 3.6 MJ = 999 860 400 J |
| S01 École | MWh | `"0.846"^^unit:MW.h` | 846 kWh |
| D01 Fromagerie | kWh | `"3387.0899999999992"^^unit:h.kW` | 3387.09 kWh (the sum is an `xsd:double`) |

### What N3 and retox get

`radeau build --emit n3-rules` writes only `producer`, `crowded_feeder` and `invalid_*` as N3 rules. retox can
count, so a `count distinct` whose aggregated variable is the block's only local variable becomes a list:

```n3
{
  ?f a community:Feeder .
  ( ?site { ?site a community:Producer . ?site community:feeder ?f . } ?_v7 ) log:collectAllIn ?_scope . ?_v7 list:length ?n .
  ?n math:notLessThan "5"^^xsd:integer .
}  => {
  ?f a community:CrowdedFeeder .
} .
```

The `sum`, `max` and `average` rules are written to N3 too (`?L math:sum ?t`, `?L math:avg ?a`).
`idle_installation`'s `count`, whose block has a second local variable (the export value), is written as a comment, `# rule …: aggregate, runs as
SHACL-AF only`, and `radeau check` warns `S020` for it. It runs only in `radeau validate` (Limitations, E).

### Stratification

The rules' `sh:order` (`radeau build --emit shacl`). A rule that aggregates over a class or property comes after
every rule that derives it, and a rule that reads a keyed class comes after that class's key rule:

| Stratum | Rules |
|---|---|
| 0 | `Feeder` and `Site` key rules, `producer`, `over_contract_6kw`, `over_contract_9kw`, `over_contract_36kw`, `low_average_school`, `invalid_reading`, `invalid_export` |
| 1 | `DailyReading` key rule (it reads `Site`'s), `monthly_import_total` (reads `Site`), `crowded_feeder` and `idle_installation` (count `Producer`s, derived in stratum 0) |

The `over_contract_*` rules aggregate readings too, but they read no class, only properties that no rule derives,
so they stay in stratum 0.

The comment block at community.dlf:183 adds a rule `crowded_members` (a site on a crowded feeder is a Producer).
`crowded_feeder` counts Producers to derive CrowdedFeeder, and `crowded_members` derives Producers from it. In a
scratch copy with that rule, `radeau build --emit shacl` reports:

```text
Error: Code generation error: Unstratifiable negation cycle through: rule crowded_feeder, rule crowded_members
```

`radeau validate` gives `Error: SHACL emission failed: Unstratifiable negation cycle through: rule crowded_feeder,
rule crowded_members`. `radeau check` exits 0 (Limitations, D).

### What fires

From `radeau validate` (SHACL-AF), on the package's facts and readings:

| Rule | Fires for | Does not fire for |
|---|---|---|
| `producer` | H01, H02, H03, H10, H11, S01, D01 | the 16 sites without an installation |
| `over_contract_*` | H08 (7.2 kW, 6 kVA), D01 (41.3 kW, 36 kVA) | H09: exactly 9.0 kW on 9 kVA, and `>` is strict |
| `crowded_feeder` | DEPART_A: exactly 5 producers, `>= 5` | DEPART_B: 2 producers |
| `idle_installation` | H10 (every export 0), H11 (no reading at all) | the other 5 producers |
| `low_average_school` | S01 (15.2 kWh per weekday since 6 July) | S02 (54.8 kWh) |
| `invalid_reading` | `validate/bad/negative_import.ttl` | every CSV reading |

## Queries

`queries/expected/` holds the tables that the harness can check today, `producers_per_feeder`,
`crowded_feeders` and `over_contract_sites`. They come from `python3 generate_readings.py --print-expected`, which
prints all six queries' expected rows. The other three return empty cells or miss the rows of a mixed-unit sum
(Limitations: hospital-pharmacy E, and B), so the harness only runs them, and the script's output is what to check
them against once fixed:

```text
== feeder_totals            DEPART_A  9247.104 kWh exported, 6728.096 kWh imported
                            DEPART_B     0.000 kWh exported, 4107.410 kWh imported
== top_consumers            Fromagerie du Glandasse 3387.09 kWh, Centre de loisirs des Tilleuls 1343.03 kWh,
                            École de Saint-Roman 0.8460 MWh, Foyer Chabert 311.13 kWh, Foyer Vial 301.32 kWh
== self_consumption         9247.104 kWh exported / 10835.506 kWh imported = 0.853
== over_contract_sites      Foyer Hugues 7.2 kW, Fromagerie du Glandasse 41.3 kW
```

`self_consumption` returns the two sums: queries have no arithmetic, so the ratio is not computed.

## Validation

`validate/now` is 2026-08-01T08:00:00Z, the morning after the month. `validate/ok/new_reading.ttl` is Foyer
Escoffier's first August reading. `validate/bad/` has one violation per file:

- `negative_import.ttl`: an import of -3.2 kWh. The rule `invalid_reading` makes it an `InvalidReading`, which
  needs a `correction` note (`MinCountConstraintComponent`).
- `energy_given_as_power.ttl`: an import of 7.42 kW, a power (`NodeConstraintComponent`, the dimension check).
- `reading_without_site.ttl`: no `site` (`MinCountConstraintComponent`).
- `duplicate_key_conflict.ttl`: Foyer Escoffier's 31 July reading sent again under a new id. Same site and day,
  so the key merges it with the CSV row. It has a different `imported` and a different `working_day`. The merge
  check reports `working_day has two values via key merge with …` (`SPARQLConstraintComponent`). It does not
  report the import (Limitations, C).

## Commands

From `rust/`:

```sh
cargo run -q -p radeau -- check examples/showcase/solar-community
cargo run -q -p radeau -- build examples/showcase/solar-community -o /tmp/solar.ttl
cargo run -q -p radeau -- build examples/showcase/solar-community --emit shacl -o /tmp/solar-shacl.ttl
cargo run -q -p radeau -- build examples/showcase/solar-community --emit n3-rules -o /tmp/solar.n3
cargo run -q -p radeau -- validate examples/showcase/solar-community --now 2026-08-01T08:00:00Z \
  --data examples/showcase/solar-community/validate/bad/negative_import.ttl
cargo run -q -p radeau -- fmt --check examples/showcase/solar-community
cargo test -p radeau --test showcase_examples
cargo test -p dolfin-lint --test fmt_examples
python3 examples/showcase/solar-community/generate_readings.py --print-expected
```

`python3 generate_readings.py` (no argument) writes `data/readings.csv` again, byte for byte.

## Limitations

The letters refer to the entries under "solar-community showcase" in `rust/BUGS.md`. Entries of other showcases are
named in full.

- **A.** `?peak [ > ?contract ]` never fires. The comparison of two quantity variables is a raw `FILTER(?peak >
  ?contract)`, which is an error on unit-typed literals, even in the same unit. `over_contract` is therefore three
  rules, one per contract level, each with a literal threshold.
- **B.** A `sum` over mixed units is in `kg.m2.s-2`, which has no `dq:` definition, so a `has monthly_import:
  energy` field would reject H07's total. `monthly_import` is a `property … -> float`, with no shape.
- **C.** The key merge's check on a `one` quantity field (`FILTER(?x != ?y)`) is an error on unit-typed literals,
  so two different imports for one site and day are not reported. Only the `working_day` conflict is.
- **D.** `radeau check` accepts a rule cycle through an aggregate. Only `build --emit shacl / n3-rules` and
  `validate` refuse it, and their message says "negation" for an aggregate.
- **E.** `count` rules with more than one local variable, and `average` rules, run in SHACL-AF only.
  `sum` and `max` run in retox.
- **F.** `radeau validate` takes about 65 s per data file in a debug build (3.5 s without the `DailyReading` key),
  and the harness runs it five times. The retox key rule had the same quadratic cost (mountain-ultra C), and is now
  joined on the object key first (`irukame/src/shacl/retox.rs`), which brought the harness's retox step from 288 s
  to 19 s.
- (hospital-pharmacy E) `sum` over a quantity in a query is unbound, so `feeder_totals` and `self_consumption`
  return empty cells. The `order` on a quantity column is lexical as well (mountain-ultra D).
- (hospital-pharmacy A, B) A `[ >= 0 ]` bound on a quantity field rejects every value, and a quantity `check` never
  fails. A negative reading is therefore caught by a rule (`invalid_reading`), whose class needs a `correction`.
- (seed-cooperative D) A comparison with a `unitdef kVA` unit compiles to a string compare. Contracts are in kW,
  read as kVA at a power factor of 1.
- `sum` over an empty group has no value (`syntax.md`, "Aggregates in rules"). `idle_installation` therefore
  counts the readings that have an export, and that count is 0 both for no readings and for all-zero readings.
- There is no day-of-week function. The CSV carries a `weekday` column, read as `working_day`.
- A `case` arm cannot hold a cell and a cast has a fixed unit, so the readings take one mapping per unit, each
  filtered with `where:`.
- Rule-derived classes are plain concepts, not `sub Site`. A rule-derived subclass of a keyed class puts the key
  rule in a later stratum: retox accepts it since 2026-11-14 (BUGS.md, high-school), SHACL refuses it.
