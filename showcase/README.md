# Showcase projects

Each `<name>/` here is checked by `cargo test -p radeau --test showcase_examples`:
`radeau check`, `radeau build` (Turtle and SHACL), then the optional files below.
Base IRI: none (as a plain `radeau build`).

A `<name>/` with no `package.dlf` holds several packages: each sub-dir that has a `package.dlf` is
checked on its own, under the name `<name>/<sub>` (`city-transit/network`, `city-transit/timetable`),
with the files below inside that sub-dir. Skips are listed at the top of the test, by that name
(`SKIP_QUERY_ROWS` runs a query but does not compare its rows).

A package that imports another one has its import lock in `.dolfin/imports/<slug>/`. The lock's
`turtle.ttl` and `closure.ttl` are added to the data of each `validate` and to the queries' store, as a
deployment loads them next to the package.

| File | Meaning |
|---|---|
| `package.dlf` + `*.dlf` | required |
| `validate/ok/*.ttl` | data that, with the package's facts, conforms: `radeau validate` exits 0, stdout empty |
| `validate/bad/X.ttl` | one violation scenario: exit 1 |
| `validate/bad/X.expect` | substrings, one per line, that must all appear in the report (stderr) |
| `validate/now` | RFC 3339 instant passed as `--now` (default `2026-06-15T12:00:00Z`) |
| `queries/expected/<query>.tsv` | expected rows of `query <query>:`; other queries only have to run |

Queries run on the built Turtle after the package rules, the concept-condition and key rules and
RDFS are materialized (retox). TSV: header = returned variables without `?`, tab-separated; values
are lexical forms or IRI local names (after the last `#` or `/`); unbound = empty cell. Rows are
compared in order when the query has an `order`, sorted otherwise.

Examples:

```turtle
# validate/bad/minor.ttl
@prefix main: <https://www.dolfin.fr/showcase/vote/main#> .
main:bob a main:Citizen ; main:birthdate "2015-01-01"^^<http://www.w3.org/2001/XMLSchema#date> .
```

```text
# validate/bad/minor.expect
CanVote: condition not met
# validate/now
2026-06-15T12:00:00Z
# queries/expected/death_figures.tsv
tradition	figure
Greek	Hades
```
