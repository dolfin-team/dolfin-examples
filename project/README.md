# Project and Task Tracker

A small data model for projects, tasks and the people who own them. It shows how to flag work that needs attention, such as a critical task with nobody assigned.

## What's inside

- **`Project`**: a body of work with an owner, an optional deadline and an `active` flag.
- **`Task`**: a unit of work in a project. It has a status, a priority, an optional assignee and can be blocked by other tasks.
- **`TaskStatus`**: `TODO`, `IN_PROGRESS`, `BLOCKED` or `DONE`.
- **`Priority`**: `Low`, `Medium`, `High` or `Critical`.
- **`Person`**: identified by email, with a first and last name.
- **Facts**: two people (`priya`, `sam`), one project (`platformRedesign`) and two tasks (`fixLoginBug`, `writeMigrationPlan`).

## Try it

- Read the rule `flag_unassigned_critical`. It marks every `Critical` task with no assignee as an `UnassignedCriticalTask`. Here, `writeMigrationPlan` matches.
- Run the query `active_project_tasks` to list all tasks on active projects.
- Run `radeau check .` to validate the package.

## Learn more

- `one of:` enumerations (`TaskStatus`, `Priority`)
- `optional` and repeatable properties (`assignee`, `blockedBy`)
- Rules that derive new facts (`?task assignee 0` means "no assignee")
