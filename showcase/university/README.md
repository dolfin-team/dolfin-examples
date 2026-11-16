# University school office (scolarité)

The school office of a fictional university licence, first year. It keeps the students, the UEs
(teaching units) of the two semesters with their planned hours, ECTS and coefficients, the marks,
the teachers and their sessions, and the absences. At the end of each semester it hands out the
bulletins, the list of students absent too often and the teachers' hours, as Excel, CSV and JSON
files built by `export` declarations. Everyone in it is invented.

## Scenario

| File | Content |
|---|---|
| `data/etudiants.csv` | 9 students. E26009 (Anaïs Delmas) is on a two-year plan (`plan` = `deux ans`) |
| `data/ue.csv` | 6 UEs, 3 per semester: code, title, semester, planned hours, ECTS, coefficient, teacher |
| `data/enseignants.csv` | 3 teachers |
| `data/absences.csv` | 14 half-day absences |
| `data/scolarite.xlsx` | sheets `Notes` (51 marks out of 20), `Pondération` (one row per coefficient point of a UE), `Séances` (71 sessions) |
| `generate_scolarite.py` | wrote `data/scolarite.xlsx` once (`uv run generate_scolarite.py`); not part of the build |
| `scolarite.dlf` | concepts, the decision table, the rules |
| `mappings.dlf` | the CSV and XLSX mappings |
| `exports.dlf` | the queries and the exports |

The marks are chosen so that every case occurs (coefficients 3, 2, 1 in each semester):

| Student | Semester 1 | Decision |
|---|---|---|
| E26001 Camille Rivière | 14, 12, 15 → 13.5 | Admis |
| E26002 Hugo Marchand | 11, **8**, 13 → 10.33 | Admis par compensation |
| E26003 Inès Lefort | 7, 9, 12 → 8.5 | Ajourné |
| E26005 Léna Brossard | 10, 10, 10 → 10 | Admis (a UE at exactly 10 is validated) |
| E26006 Nathan Perrot | 13, **7**, **7** → 10 (unweighted: 9) | Admis par compensation |
| E26009 Anaïs Delmas | MATH1 and ANGL1 only | no decision: two-year plan |

MATH1 was taught 64 h for 60 planned (over), BDD2 36 h for 40 (under); the other UEs as planned.
Hugo was absent on 4 days and Malo on 3 (one of them morning and afternoon): both are flagged. Inès
has 3 half-day absences on only 2 days and is not.

## Rules (MCC, kept simple)

- A mark below 10 makes the `Note` a `NoteInsuffisante` (the UE is not validated).
- Per enrolment (student × semester), `count distinct` of the `NoteInsuffisante`s gives the
  enrolment's `bilanUE`: `ToutesValidees` (0) or `AvecUENonValidee` (≥ 1).
- The semester decision comes from the decision table (`Decision` facts): average in
  [10, 20.5) with all UEs validated is "Admis", with a UE below 10 "Admis par compensation", and
  an average below 10 "Ajourné".
- `count distinct` absence days ≥ 3 makes the student `AbsencesRepetees`.
- `planAnnee DeuxAns` makes the student `EtudiantAmenage`: left out of the standard bulletins,
  listed with their marks in the `Aménagements` sheet.

### Why the averages are queries

The weighted averages and the hours taught are computed in the queries, not in rules. The language
has no arithmetic in queries, so the average is weighted by joining each mark with the coefficient
points of its UE (`Ponderation`): a coefficient-3 mark appears three times, and the plain `average`
of the joined rows is the weighted one. The query compares the average to the bands of the decision
table (`?moyenne >= ?min`, `?moyenne < ?max`) instead of an if/else.

The sessions keep their length twice: `duree` (a duration, `as quantity(h)`) and `heures` (a
float), because a query `sum` of durations has no value (see `rust/BUGS.md`). The hours are summed
from `heures`; the `Séances` sheet writes `duree` back with the `quantity(h)` cast.

The package has no `has key`: keys and the rules concluding sub-concepts of keyed concepts hit
the retox stratification issue noted for `high-school` and `wolf-tracking` in `rust/BUGS.md`. The
IRIs are built from the numbers, so nothing needs merging.

## Exports

| File | Sheets / form | Source |
|---|---|---|
| `bulletins.xlsx` | `Semestre 1`, `Semestre 2`, `Aménagements` | named queries `bulletin_s1`, `bulletin_s2`, `amenagements`, French headers in `map:` |
| `absences.csv` | UTF-8 with BOM | inline `from:` with a `count distinct` |
| `heures-enseignants.xlsx` | `Service`, `Séances` (`quantity(h)` cast), `Dépassements`, `Sous-service` | `service`, `seances`, and two queries composed on `service` |
| `resultats-s1.json` | `{"etudiants": [{"numero", "identite": {…}, "semestre1": {…}}]}` | `bulletin_s1`, `for each "$.etudiants[*]"` |

## Commands

```bash
cd rust
cargo run -p radeau -- check examples/showcase/university
cargo run -p radeau -- export examples/showcase/university --out /tmp/univ-out --now 2026-06-15T12:00:00Z
cargo test -p radeau --test university_export
```
