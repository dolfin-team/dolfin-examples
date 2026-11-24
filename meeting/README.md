# Meeting

A small data model for scheduled meetings, their organizers and invitees. It also has one rule that flags retros with no agenda.

## What's inside

- **`MeetingType`**: a fixed list of meeting kinds (`STANDUP`, `PLANNING`, `ONE_ON_ONE`, `RETRO`, `ALL_HANDS`), each with a `code`.
- **`RSVPStatus`**: an invitee's answer: `Pending`, `Accepted`, `Declined` or `Tentative`.
- **`Person`**: identified by `email`, with a first and last name.
- **`Invitation`**: one invitee (`attendee`) and their `status`.
- **`Meeting`**: identified by `title`. It has an `organizer`, a `type`, start and end times, and one or more `invitations`. `location`, `agenda` and `notes` are optional.
- **`NeedsFollowUp`**: a tag that the rule below puts on meetings.
- **Facts**: two people (`priya`, `sam`) and two meetings (`standup`, `retro`).

## Try it

- Read the rule `flag_missing_agenda`. It finds every `RETRO` meeting with no `agenda` and marks it `NeedsFollowUp`.
- Look at the facts `standup` and `retro`. Only `retro` has an agenda, so the rule does not flag it. Delete its `agenda` line to see it flagged.

## Learn more

- `one of:` enumerations (`MeetingType`, `RSVPStatus`)
- `optional`, `one` and `some` property cardinalities on `Meeting`
- A rule that matches a missing property with `agenda 0`
