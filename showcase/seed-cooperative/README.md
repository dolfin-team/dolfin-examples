# Seed-swap cooperative

Graines du Vercors (fictional) is a cooperative of fifteen small farms in the Vercors massif, from
Villard-de-Lans to Saint-Jean-en-Royans, that keep heirloom seed varieties alive by growing them and swapping
lots of them. A **lot** is one farm's stock of one variety from one harvest. It is counted in the unit that suits
the crop:

- grain and beans by mass, in kg or g;
- tomato, lettuce and carrot seed in **packets**;
- garlic in **bulbs**;
- potatoes in **tubers**.

Farms pay each other in the cooperative's own credit, the **graine**: 1 graine = 0.50 EUR. A variety is identified
by its species and its name. Farms file varieties under catalogue codes, and two of them filed a variety the
cooperative already had under a new code. The two-field key makes those records the same variety.

The coordinators want to know which varieties only one farm holds (lose that farm and the variety is gone), which
of those germinate poorly and must be regrown first, who has been active in the last twelve months, and who gives
the most.

Data (`data/`, described in `data/README.md`): 15 farms, 22 variety records of 20 varieties in 7 species, 60 lots,
and a 30-exchange book in a spreadsheet.

## Feature map

| Feature | Where | Compiles to |
|---|---|---|
| Derived currency unit `unitdef graine: scale 0.5 EUR` | units.dlf:20 | `<https://dolfin.dev/unit/graine> dq:coefficient 0.5`; prices `"6"^^<https://dolfin.dev/unit/graine>` |
| Nominal units, one family each | units.dlf:32-42 | `dq:dimension "1"` (see Limitations, C); counts `"12"^^<https://dolfin.dev/unit/packet>` |
| Nominal-mixing error | units.dlf:3-15 (comment) | `error[S007]` at check time, see below |
| `one of:` with fixed key values | coop.dlf:8-18 (`Species`) | `owl:oneOf ( coop:Species_TOMATO … )`, `coop:Species_TOMATO coop:latin_name "Solanum lycopersicum"` |
| Two-field `key:` block | coop.dlf:23 (`Variety`) | `owl:hasKey ( coop:species coop:name )`; SHACL rule `CONSTRUCT { $this owl:sameAs ?o }` |
| `set of string` | coop.dlf:28, 30 | multi-valued property, no `sh:maxCount` |
| Bounded `int` / `float` | coop.dlf:31, 51-52 | `sh:minInclusive` / `sh:maxInclusive` |
| Dimension-typed field `mass: optional mass` | coop.dlf:56 | `sh:node [ sh:sparql … dq:dimension "M1" … ]` (metres: violation) |
| `check` on a year | coop.dlf:63 | `sh:sparql` `FILTER(!(?harvest_year <= "2026"^^xsd:integer))` (`Lot: condition not met`) |
| `check` with `$` (from ≠ to) | coop.dlf:79 | `sh:sparql` `FILTER(!(?to != ?from))` (`Exchange: condition not met`) |
| `property … -> float` for nominal / currency values | coop.dlf:69, 83 | `owl:DatatypeProperty ; rdfs:range xsd:double`, no shape |
| Rule with `none` and `!=` between variables | coop.dlf:96 (`rare_variety`) | N3 `log:notIncludes { ?o coop:variety ?v . ?o coop:holder ?_v1 . ?_v1 log:notEqualTo ?f . }` |
| Rule over an inferred class | coop.dlf:107 (`seed_bank_candidate`) | `?_v2 a coop:RareVariety . ?_v3 math:lessThan "0.6"^^xsd:float` |
| Rule with a path `from\|to` and a date bound | coop.dlf:115 (`active_member`) | `?e coop:from\|coop:to ?f . ?_v4 math:notLessThan "2025-06-15"^^xsd:date` |
| CSV mapping, `as date` | mappings.dlf:5 | `coop:joined "2012-03-10"^^xsd:date` |
| `case` value table | mappings.dlf:34 (species), 68 (unit) | `coop:species coop:Species_TOMATO`; `coop:counted_in coop:CountUnit_PACKET` |
| `slug()` in IRIs | mappings.dlf:32, 62, 141 | `seed:lot_gv_2024_003` from `GV-2024-003` |
| `where:` + `as quantity(<unit>)`, one mapping per unit | mappings.dlf:73-126 | `"800"^^<https://dolfin.dev/unit/g>`, `"40"^^<https://dolfin.dev/unit/bulb>` |
| XLSX mapping, date cells, `as quantity(graine)` | mappings.dlf:131 | `coop:exchanged_on "2025-01-18"^^xsd:date`; empty price → no triple |
| `group by` + `count distinct` | queries.dlf:13 | `COUNT(DISTINCT ?name)` |
| Per-row `count`, two `order`s, `limit` | queries.dlf:37-44 | subquery `COUNT(?e)` … `ORDER BY DESC(?exchanges) ASC(?farm) LIMIT 5` |
| External IRI in a query (`prefix … as owl`) | queries.dlf:4, 67 | `?_v owl:sameAs ?_v0` |

## Custom units

```dolfin
unitdef graine: scale 0.5 EUR

unitdef family packets

unitdef packet: nominal of packets scale 1

unitdef family bulbs

unitdef bulb: nominal of bulbs scale 1

unitdef family tubers

unitdef tuber: nominal of tubers scale 1
```

The graine is a **derived** unit on the currency axis, like `USD` in `examples/finance`: `quantity(10 graine as EUR)`
is 5 EUR. Packets, bulbs and tubers are **nominal** units: they have no dimension and no conversion between them.
Each one has its own family. With one shared `seedlots` family, `quantity(3 packet + 2 bulb as seedlots)` builds as
`"5"^^<https://dolfin.dev/unit/seedlots>`, which adds packets of lettuce to bulbs of garlic. With one family per
unit, no cast can add them.

`radeau build examples/showcase/seed-cooperative` emits this definition block (copied from the output; `g` and `kg`
come from the masses):

```turtle
# Quantity unit definitions
<https://dolfin.dev/unit/bulb> dq:coefficient 1 ; dq:dimension "1" ; dq:symbol "bulb" .
<https://dolfin.dev/unit/g> dq:coefficient 0.001 ; dq:dimension "M1" ; dq:symbol "g" .
<https://dolfin.dev/unit/graine> dq:coefficient 0.5 ; dq:dimension "1" ; dq:symbol "graine" .
<https://dolfin.dev/unit/kg> dq:coefficient 1 ; dq:dimension "M1" ; dq:symbol "kg" .
<https://dolfin.dev/unit/packet> dq:coefficient 1 ; dq:dimension "1" ; dq:symbol "packet" .
<https://dolfin.dev/unit/tuber> dq:coefficient 1 ; dq:dimension "1" ; dq:symbol "tuber" .
```

Mixing two nominal units is rejected when the package is checked. In a scratch file next to the package:

```dolfin
fact l a coop.Lot
  counted quantity(3 packet + 2 bulb)
```

`radeau check` reports:

```text
error[S007]: invalid quantity literal: Incommensurable units: cannot add packet and bulb directly — cast with `as <family>` first
```

`quantity(3 packet + 2 bulb as packets)` gives the same error, because `bulb` is not in `packets`. A mass in metres
(`mass quantity(2 m)`) gives `error[S008]: dimension mismatch: `mass` expects a Mass quantity, found Length`.

What SPARQL sees for a count is a literal whose datatype is the unit IRI: `"12"^^<https://dolfin.dev/unit/packet>`.
The query `lots_in_packets` cannot filter on that literal (Limitations, D), so the lot mapping also records the unit
as a `CountUnit` member (`coop:counted_in coop:CountUnit_PACKET`) and the query selects on that member.

## Commands

From `rust/`:

```sh
cargo run -q -p radeau -- check examples/showcase/seed-cooperative
cargo run -q -p radeau -- build examples/showcase/seed-cooperative -o /tmp/seeds.ttl
cargo run -q -p radeau -- build examples/showcase/seed-cooperative --emit shacl -o /tmp/seeds-shacl.ttl
cargo run -q -p radeau -- validate examples/showcase/seed-cooperative --now 2026-06-15T12:00:00Z \
  --data examples/showcase/seed-cooperative/validate/bad/self_exchange.ttl
cargo run -q -p radeau -- fmt --check examples/showcase/seed-cooperative
cargo test -p radeau --test showcase_examples
cargo test -p dolfin-lint --test fmt_examples
```

To regenerate the spreadsheet (byte-identical), run `uv run generate_exchanges.py` from this directory.

`validate/ok/new_member.ttl` has a sixteenth farm that joins, deposits a lot and buys one. `validate/bad/` has one
violation per file:

- a germination rate of 1.3;
- a lot from the 2027 harvest;
- an exchange from a farm to itself;
- a lot without a holder;
- a lot weighed in metres.

`queries/expected/` was worked out by hand from `data/` and checked against the harness. The harness runs on the
default `--now 2026-06-15T12:00:00Z`.

- `rare_varieties` has 10 rows. The query merges keyed records, so Rose de Lautrec is listed once per holder of
  either record, and Noire de Crimée (TOM-CRIMEE is rare) also lists the two holders of its twin TOM-NC.
- `urgent_regeneration` has the three rare lots under 0.6.
- `active_members` lists the 13 farms with an exchange since 2025-06-15. Les Semences de Vassieux and La Ferme
  d'Engins have none.

## Limitations

The letters refer to the entries under "seed-cooperative showcase" in `rust/BUGS.md`.

- **A.** No field type accepts a packet, bulb, tuber or graine quantity. A `has … float` field rejects them in
  SHACL, although the docs say `float` takes any quantity. No dimension name exists for a currency or a family.
  `counted` and `price` are therefore `property … -> float`: they have an OWL range and are not validated.
- **B.** Only a `date_time` compares with `now()`. `[ harvest_year [ <= now() ] ]` compiles but never fails, and
  there is no year function. The harvest check therefore uses the literal year 2026, consistent with the harness's
  `--now`. A field bound `[ <= now() ]` is silently dropped.
- **C.** The `dq:` block gives the graine and the three nominal units the same dimension, `"1"`. A unit-aware
  comparison cannot tell them apart.
- **D.** `counted [ > quantity(0 packet) ]` in a query compiles to a comparison with the string `"0 packet"`.
  Built-in units unfold through `dq:`. `lots_in_packets` uses the `CountUnit` member instead.
- **E.** "Exactly one of `mass` and `counted`" cannot be checked. Conditions have no `or`, `exactly 1` counts one
  property, and validation does not follow `sub` properties. The package has no such check.
- **mountain-ultra C.** Rules do not act on the inferred `owl:sameAs`, queries do. The two Rose de Lautrec records
  both stay `RareVariety`, each with its own holder, and TOM-CRIMEE is rare while TOM-NC is not.
  `varieties_per_species` counts distinct names so that the duplicates count once. Unlike in mountain-ultra,
  `owl:sameAs` can be queried here, through `prefix <http://www.w3.org/2002/07/owl#> as owl`.
- Rules have no aggregates and no `now()`. "Held by one farm" is a `none` block, and the twelve months of
  `active_member` end at the literal date 2025-06-15.
- `RareVariety` is a plain concept, not `sub Variety`. A key's `owl:sameAs` rule that depends on a rule with a
  quantifier is refused by retox (BUGS.md, high-school), and the harness skips that showcase's queries for this
  reason.
- `date` and `count` are keywords where a field name is expected, so the fields are `exchanged_on` and `counted`.
- A `case` arm cannot hold a cell, and a cast has a fixed unit. The lots therefore take five amount mappings, one per
  `unit`, each filtered with `where:`.
- The spreadsheet mapping is radeau only: the browser playground has no XLSX reader.
