# Team

A small org-chart model: people, roles, and a team with a lead. It shows how to describe who works where and who reports to whom.

## What's inside

- **`Role`**: a fixed list of roles (`ENGINEER`, `DESIGNER`, `PRODUCT_MANAGER`, `LEAD`), each with a `code`.
- **`Person`**: identified by `email`, with a first name, last name and one `role`.
- **`Team`**: identified by `name`, with exactly one `lead` and at least one member (`some Person`).
- **`reports_to`**: a link from one `Person` to another, the formal org-chart line.
- **Facts**: `priya` (the lead), `sam` and `lea` (who report to Priya), and `platformTeam` with all three as members.

## Try it

Open `team.dlf` and read the `platformTeam` fact. Then look at `sam`: its `reports_to priya` line is the org chart in one word.

```dolfin
fact sam a Person
  email "sam@example.com"
  role ENGINEER
  reports_to priya
```

## Learn more

- `one of:` enumerations (`Role`)
- Cardinalities: `one` and `some`
- Custom `property` between concepts (`reports_to`)
