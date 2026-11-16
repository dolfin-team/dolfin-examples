"""Generate data/readings.csv, the community's smart-meter readings for July 2026, once.

    python3 generate_readings.py                   # (re)write data/readings.csv
    python3 generate_readings.py --print-expected  # print queries/expected/*.tsv

The Dolfin package only reads the CSV (readings.dlf); this script is not part
of the build. Seeded: re-running it writes the same bytes. The sites below
mirror the facts at the bottom of community.dlf.

Energies are drawn in whole Wh, then written in the meter's unit: Wh as an
integer, kWh with 2 decimals (multiples of 10 Wh), MWh with 4 decimals
(multiples of 100 Wh). Every value is exact, so the sums printed by
--print-expected are exact too.
"""
import csv
import datetime
import random
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "data" / "readings.csv"
EXPECTED = HERE / "queries" / "expected"
MONTH = [datetime.date(2026, 7, d) for d in range(1, 32)]
SCHOOL_HOLIDAYS = datetime.date(2026, 7, 4)  # the école closes after Friday 3 July
METER_SWAP = datetime.date(2026, 7, 16)  # H07's Wh meter is replaced by a kWh one

# code: (pdl, kind, feeder, contracted power in kW (kVA at cos φ = 1), meter unit, PV kWc or None)
SITES = {
    "H01": ("26140000000101", "HOUSEHOLD", "DEPART_A", 9, "Wh", 6),
    "H02": ("26140000000102", "HOUSEHOLD", "DEPART_A", 6, "Wh", 3),
    "H03": ("26140000000103", "HOUSEHOLD", "DEPART_A", 9, "kWh", 9),
    "H04": ("26140000000104", "HOUSEHOLD", "DEPART_A", 6, "Wh", None),
    "H05": ("26140000000105", "HOUSEHOLD", "DEPART_A", 6, "kWh", None),
    "H06": ("26140000000106", "HOUSEHOLD", "DEPART_A", 9, "kWh", None),
    "H07": ("26140000000107", "HOUSEHOLD", "DEPART_A", 6, "Wh/kWh", None),
    "H08": ("26140000000108", "HOUSEHOLD", "DEPART_A", 6, "kWh", None),
    "H09": ("26140000000109", "HOUSEHOLD", "DEPART_A", 9, "kWh", None),
    "S01": ("26140000000201", "SCHOOL", "DEPART_A", 36, "MWh", 36),
    "D01": ("26140000000301", "DAIRY", "DEPART_A", 36, "kWh", 30),
    "H10": ("26140000000110", "HOUSEHOLD", "DEPART_B", 6, "kWh", 3),
    "H11": ("26140000000111", "HOUSEHOLD", "DEPART_B", 9, "kWh", 6),
    "H12": ("26140000000112", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H13": ("26140000000113", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H14": ("26140000000114", "HOUSEHOLD", "DEPART_B", 9, "kWh", None),
    "H15": ("26140000000115", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H16": ("26140000000116", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H17": ("26140000000117", "HOUSEHOLD", "DEPART_B", 9, "kWh", None),
    "H18": ("26140000000118", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H19": ("26140000000119", "HOUSEHOLD", "DEPART_B", 6, "kWh", None),
    "H20": ("26140000000120", "HOUSEHOLD", "DEPART_B", 9, "kWh", None),
    "S02": ("26140000000202", "SCHOOL", "DEPART_B", 9, "kWh", None),
}
NO_READINGS = {"H11"}  # PV commissioned 20 July, meter not yet on the data hub
INVERTER_FAULT = {"H10"}  # PV installed, inverter down all month: every export is 0
# The highest daily peak of these sites, in kW (every other day stays below it).
FORCED_PEAK = {
    "H08": (datetime.date(2026, 7, 14), Decimal("7.2")),  # 6 kVA contract: over
    "H09": (datetime.date(2026, 7, 21), Decimal("9.0")),  # 9 kVA contract: exactly at it, not over
    "D01": (datetime.date(2026, 7, 8), Decimal("41.3")),  # 36 kVA contract: over (cheese-making day)
}

rng = random.Random(2026)


def wh(lo_kwh, hi_kwh, step):
    """A random energy in Wh between lo and hi kWh, a multiple of `step` Wh."""
    return rng.randrange(int(lo_kwh * 1000) // step, int(hi_kwh * 1000) // step + 1) * step


def reading(code, day):
    pdl, kind, _feeder, contract, unit, kwc = SITES[code]
    unit = ("Wh" if day < METER_SWAP else "kWh") if unit == "Wh/kWh" else unit
    step = {"Wh": 1, "kWh": 10, "MWh": 100}[unit]
    weekday = day.weekday() < 5
    if kind == "SCHOOL" and code == "S01":
        imported = wh(120, 160, step) if weekday and day < SCHOOL_HOLIDAYS else wh(10, 20, step)
        peak = Decimal(rng.randrange(180, 300)) / 10 if weekday and day < SCHOOL_HOLIDAYS else Decimal(rng.randrange(30, 60)) / 10
    elif kind == "SCHOOL":  # the summer day-camp, open on weekdays
        imported = wh(45, 70, step) if weekday else wh(8, 12, step)
        peak = Decimal(rng.randrange(40, 85)) / 10
    elif kind == "DAIRY":
        imported = wh(80, 140, step)
        peak = Decimal(rng.randrange(250, 340)) / 10
    else:
        imported = wh(4, 14, step)
        peak = Decimal(rng.randrange(20, 55)) / 10
    exported = 0
    if kwc and code not in INVERTER_FAULT:
        # July in the Diois: 4.5 to 6 kWh per kWc and per day, minus self-consumption.
        exported = wh(kwc * 2.5, kwc * 4.5, step)
    if code in FORCED_PEAK and FORCED_PEAK[code][0] == day:
        peak = FORCED_PEAK[code][1]
    return {"pdl": pdl, "day": day.isoformat(), "weekday": str(weekday).lower(), "unit": unit,
            "imported": imported, "exported": exported, "peak_kw": peak.quantize(Decimal("0.1"))}


def fmt(energy_wh, unit):
    return str({"Wh": Decimal(energy_wh), "kWh": Decimal(energy_wh) / 1000, "MWh": Decimal(energy_wh) / 1000000}[unit]
               .quantize({"Wh": Decimal(1), "kWh": Decimal("0.01"), "MWh": Decimal("0.0001")}[unit]))


ROWS = [reading(code, day) for day in MONTH for code in SITES if code not in NO_READINGS]


def write_csv():
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["pdl", "day", "weekday", "unit", "imported", "exported", "peak_kw"])
        for r in ROWS:
            w.writerow([r["pdl"], r["day"], r["weekday"], r["unit"], fmt(r["imported"], r["unit"]),
                        fmt(r["exported"], r["unit"]), r["peak_kw"]])
    print(f"wrote {OUT}: {len(ROWS)} readings of {len(SITES) - len(NO_READINGS)} sites")


def kwh(energy_wh):
    return str((Decimal(energy_wh) / 1000).quantize(Decimal("0.001")))


def native_sum(code):
    """What the rule `monthly_import_total` materialises: the sum in the meter's
    unit, or in J (kg.m2.s-2) when the month mixes units."""
    rows = [r for r in ROWS if r["pdl"] == SITES[code][0]]
    units = {r["unit"] for r in rows}
    total = sum(r["imported"] for r in rows)
    if len(units) > 1:
        return f"{total * 3600} J"
    (unit,) = units
    return f"{fmt(total, unit) if unit != 'kWh' else Decimal(total) / 1000} {unit}"


def print_expected():
    """Every query's rows as the engine should return them. Only the tables
    in COMMITTED are in queries/expected/: the other queries return empty
    cells or no rows today (README, Limitations), so the harness only runs
    them, and this is the reference to check them against once fixed."""
    names = dict(re.findall(r'fact site_(\d+) a Site\n  pdl "\d+"\n  name "([^"]+)"',
                            (HERE / "community.dlf").read_text(encoding="utf-8")))
    code_of = {v[0]: k for k, v in SITES.items()}
    tables = {}
    feeders = sorted({v[2] for v in SITES.values()})
    tables["feeder_totals"] = [["feeder", "exported_kWh", "imported_kWh"]] + [
        [f, kwh(sum(r["exported"] for r in ROWS if SITES[code_of[r["pdl"]]][2] == f)),
         kwh(sum(r["imported"] for r in ROWS if SITES[code_of[r["pdl"]]][2] == f))] for f in feeders]
    monthly = {c: sum(r["imported"] for r in ROWS if r["pdl"] == SITES[c][0]) for c in SITES if c not in NO_READINGS}
    top = sorted(monthly, key=lambda c: -monthly[c])[:5]
    tables["top_consumers"] = [["name", "total", "total_kWh"]] + [[names[SITES[c][0]], native_sum(c), kwh(monthly[c])] for c in top]
    exported = sum(r["exported"] for r in ROWS)
    imported = sum(r["imported"] for r in ROWS)
    tables["self_consumption"] = [["exported_kWh", "imported_kWh", "exported_per_imported"]] + [
        [kwh(exported), kwh(imported), str((Decimal(exported) / imported).quantize(Decimal("0.001")))]]
    peaks = {c: max(r["peak_kw"] for r in ROWS if r["pdl"] == SITES[c][0]) for c in monthly}
    over = sorted((names[SITES[c][0]], c) for c in peaks if peaks[c] > SITES[c][3])
    tables["over_contract_sites"] = [["name", "peak"]] + [[n, str(peaks[c])] for n, c in over]
    producers = defaultdict(set)
    for c, v in SITES.items():
        if v[5]:
            producers[v[2]].add(c)
    tables["producers_per_feeder"] = [["feeder", "producers"]] + [[f, str(len(producers[f]))] for f in feeders if len(producers[f]) >= 3]
    tables["crowded_feeders"] = [["feeder"]] + [[f] for f in feeders if len(producers[f]) >= 5]
    for name, rows in tables.items():
        state = "committed" if name in COMMITTED else "not committed"
        print(f"== queries/expected/{name}.tsv ({state})")
        print("\n".join("\t".join(r) for r in rows))


# The tables the harness can compare today (see print_expected).
COMMITTED = {"producers_per_feeder", "crowded_feeders", "over_contract_sites"}


if __name__ == "__main__":
    if "--print-expected" in sys.argv:
        print_expected()
    else:
        write_csv()
