# Academic

A small university data model: students, instructors, courses and enrollments. Two rules derive new facts, such as which courses are advanced and which students are honors students.

## What's inside

- **`Student`, `Instructor`**: people, each with a key (`studentId`, `employeeId`) and a `Department`.
- **`Course`**: has a title, credits, an instructor and `prerequisites`. A course can have several prerequisites.
- **`Enrollment`**: links a student to a course for one `term`, with an optional `Grade`.
- **`Department`, `Grade`**: fixed lists written with `one of:` (`CS`, `MATH`, `PHYSICS` and `A` to `F`).
- **Facts**: Alan Turing teaches `CS101` and `CS301`. Ada Lovelace took `CS101` in 2026-Spring and got an `A`.
- **Rules**: `flag_advanced_course` and `flag_honors_student`.

## Try it

- Run the query `enrollments_by_term`. It lists every enrollment in `2026-Spring` with its student and course.
- Read `flag_advanced_course`. Any course with a prerequisite becomes an `AdvancedCourse`, so `algorithms` (CS301) qualifies and `intro_cs` does not.
- Read `flag_honors_student`. An enrollment with grade `A` makes its student an `HonorsStudent`, so `ada` qualifies.

## Learn more

- `one of:` enumerations for `Grade` and `Department`.
- `optional` and repeatable fields (`grade`, `prerequisites`).
- Rules that tag facts with a new concept.
