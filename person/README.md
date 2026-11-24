# Person

A small, standalone model of a person: who they are and how to reach them. It is meant to be shared by other examples (team, project, meeting) once Dolfin supports imports.

## What's inside

- **`Person`**: a human, identified by `email`. Has a first name, last name, preferred contact method, and an optional `phone` and `timezone`.
- **`ContactMethod`**: a fixed list of ways to reach someone: `EMAIL`, `PHONE`, `CHAT`.
- **Facts**: three sample people, `priya`, `sam` and `lea`.

## Try it

- Open `person.dlf` and read the `Person` concept. `has key email: string` makes the email the unique ID.
- Look at the fact `priya`. It sets `preferredContact CHAT` and leaves `phone` out, because `phone` is optional.
- Run `radeau check person` to check the project. It should report 2 concepts and no linting issues.

## Learn more

- `one of:` enumerations (see `ContactMethod`)
- `one` vs `optional` properties
