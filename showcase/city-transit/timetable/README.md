# City Transit: Timetable

The operations side of Réseau Lumière, a fictional transit network. It reads service journeys from an XML export and links them to the lines and stops of the imported `network` package (version 2.1.0).

## What's inside

- **`ServiceJourney` and `PassingTime`**: a trip on a line, and each call it makes at a stop with a departure time and an optional dwell time.
- **`VehicleType`**: four vehicles (`CITADIS_302`, `CITADIS_402`, `ARTICULATED_BUS`, `STANDARD_BUS`) with capacity, length, top speed and low-floor flag.
- **`LowFloorJourney`**: inferred from the vehicle type. A check says it may only call at accessible stops.
- **`Disruption`**: four dated disruptions. `OpenDisruption` and `CurrentDisruption` pick the ones active at `now()`.
- **Rules**: `affected_journey` and `affected_journey_bounded` mark a `DisruptedJourney`. `interchange` marks a stop served by at least 2 lines.
- **`mappings.dlf`**: turns `data/timetable.xml` into journeys and passing times.
- **`validate/`**: `bad/` and `ok/` Turtle files, such as `dwell_too_long` and `stop_not_on_line`.

## Try it

- Run the query `interchanges`. It counts the lines at each stop, busiest first.
- Run `disrupted_journeys_now`. With the pinned clock in `validate/now` (2026-06-23 07:45 UTC), only disruption D-0412 is active.
- Read the `check` in `PassingTime`. It makes sure each stop is one the journey's line serves.

Other queries: `lines_at_stop`, `first_departures`, `capacity_per_line`. Expected results are in `queries/expected/`.

## Learn more

- Importing another package at a pinned version and using its names as `net:Stop`.
- `equivalent to` concepts, `one of:` enumerations, and `case` in mappings.
