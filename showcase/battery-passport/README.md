# Digital Battery Passport

A model of the data a manufacturer must publish for each EV, industrial and light-transport battery sold in the EU from February 2027. It follows Regulation (EU) 2023/1542, Annex XIII. All manufacturers and batteries are fictional.

## What's inside

All in `battery.dlf`.

- **`Battery`**: one physical battery, with a unique `passportId`, a plant, a build date, a state of health and a `status`.
- **`BatteryModel`**: the design: category, `Chemistry`, rated energy, mass, cycle life and hazardous substance.
- **`CarbonFootprint`**: total and per-kWh footprint, plus a `FootprintClass` from `ClassA` to `ClassE`.
- **`RecycledContent`**: the share of a `CriticalMaterial` (cobalt, lithium, nickel, lead) that is recycled.
- **`Manufacturer`, `ManufacturingPlant`, `Country`**: who built it, and where.
- **Sample data**: 8 battery models and 27 batteries (`battery_001` to `battery_027`).

## Try it

- Read the rule `second_life_candidate`. It flags used EV batteries (`Original` status) with state of health from 70 % up to, but not including, 85 %. They are good for repurposing.
- Read the rule `low_carbon_model`. It flags models at or below 60 kg CO2e per kWh.
- Open `queries.md` and paste the SPARQL queries into the SPARQL tab of the public project. They cover:
  - carbon footprint per kWh, best first;
  - which models meet the 2031 recycled-content targets;
  - batteries per country of manufacture.

## Learn more

- `one of:` enumerations, such as `BatteryStatus` and `FootprintClass`.
- Units of measure: `quantity(75 kW.h)`, `quantity(480 kg)`.
- Range conditions in a rule: `[ >= 70.0, < 85.0 ]`.
