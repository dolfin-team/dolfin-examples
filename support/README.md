# Support Tickets and SLA Escalation

A small support-desk model: tickets, customers and agents. Rules flag tickets that breach their SLA (the promised response time), need escalation, or have nobody assigned.

## What's inside

- **`Ticket`**: a support request with a customer, subject, `priority`, `status`, `hoursOpen` and an optional `assignedAgent`.
- **`TicketPriority`** and **`TicketStatus`**: fixed lists of values (`LOW` to `URGENT`, `OPEN` to `CLOSED`).
- **`Agent`** and **`Customer`**: the people involved. A customer has a `tier`.
- **Facts**: `loginOutage` (urgent, open 5 hours, assigned to `maria`) and `minorTypo` (low priority, open 40 hours, unassigned).
- **Rules**:
  - `flag_sla_breach`: urgent, open tickets older than 2 hours become `SLABreach`.
  - `flag_needs_escalation`: high-priority tickets older than 24 hours become `NeedsEscalation`.
  - `flag_unassigned`: open tickets with no agent become `Unassigned`.

## Try it

- Run the query `breached_tickets`. It should list `loginOutage` with its customer `acme`.
- Read `flag_unassigned` in `support.dlf`. It uses `?t assignedAgent 0` to say "no agent set".
- Change `hoursOpen` of `loginOutage` to 1 and see the breach disappear.

## Learn more

- `one of:` enumerations for priority and status.
- `optional` properties and rules that derive new labels from facts.
