# High School Timetable and Marks

A French lycée modelled from CSV and Excel files: teachers, students, classes, rooms, a weekly timetable and a term's marks. Rules catch timetable mistakes. An absence is kept apart from a zero.

## What's inside

- **`school.dlf`**: concepts (`Teacher`, `Student`, `SchoolClass`, `HalfGroup`, `Room`, `Subject`, `Lesson`, `Slot`), mappings from `data/*.csv`, and the timetable rules.
- **`marks.dlf`**: `Test` and `TestResult` read from the Excel gradebook `data/marks.xlsx`. A missed test is an `Absence` with no mark.
- **`queries.dlf`**: `term_averages` and `absences_per_student`.
- **`generate_marks.py`**: the script that wrote the workbook once. The package only reads it.

## Try it

`data/timetable.csv` ends with five deliberate mistakes, L034 to L038. The rules flag them:

- `room_clash`: two lessons in R101 on Tuesday, period 3 (L034, L035).
- `unqualified_teacher`: a French teacher teaching mathematics (L036).
- `split_subject_for_whole_class`: physics-chemistry for the whole of 2B (L037).
- `wrong_room_kind`: mathematics in a lab (L038).

Run `term_averages`. Absences are left out of the average instead of counting as 0.

## Learn more

- `one of:` enumerations (`Day`, `RoomKind`) and `sub` concepts (`SchoolClass`, `HalfGroup`).
- `none` in `unqualified_teacher`, and `average` and `count` in queries.
- `XLSX` mappings with `sheet`, `header row 3` and `where:` filters.
