# Réseau Lumière: network

The stops and lines of a fictional French city's tram and bus network. It is the infrastructure half of a pair: the timetable package imports it.

## What's inside

- **`Stop`**: a place where vehicles call. It has a `stop_code` key, a name, coordinates, a `zone` and an `accessible` flag (step-free access).
- **`Line`**: a tram or bus line with a `code`, a `mode` and a `length` in km. There are five: `T1`, `T2`, `T3`, `B10`, `B11`.
- **`FareZone`** and **`Mode`**: fixed lists of values (`Z1`/`Z2`/`Z3`, `TRAM`/`BUS`/`BRT`).
- **`serves`**: links a line to its stops. `served_by` is its inverse, so you only write one side.
- **`connected_to`**: a walkway between two stops. It is `symmetric`, so you write it once.
- **`reachable_from`**: walking through one or more walkways. It is `transitive`, so Hôtel de Ville reaches Pont des Arts through the chain of walkways.

## Try it

- Read `network.dlf` and look at the fact `GAR`. It is an interchange for `T1`, `T2` and `B10`.
- Look at the `lat` and `long` ranges on `Stop`, such as `[ >= -90, <= 90 ]`.
- Open `validate/bad/latitude_out_of_range.ttl`. It has a stop with latitude 145.7598. The matching `.expect` file holds the error: `Value is not <= "90"`.

## Learn more

- `one of:` enumerations (`FareZone`, `Mode`)
- `inverse of`, `symmetric`, `transitive` and `sub` on properties
- Numeric range checks on values
