"""Generate the wolf-tracking data: data/collars.csv and data/ranger-2026-07-12.gpx.

    python3 generate_fixes.py                   # write the two data files
    python3 generate_fixes.py --print-expected  # write queries/expected/*.tsv

Stdlib only, seeded: a rerun writes byte-identical files. The Dolfin package
only reads the results (mappings.dlf); this script is not part of the build.

What it writes:
- 4 collared wolves x 5 days (8-12 July 2026) x 12 fixes (every 2 h, UTC):
  random walks in each pack's home range, kept out of the alpages and the
  villages, so every alpage visit is one of the scripted ones in SCRIPT.
  Five days, not a month: the Fix key (collar + at) makes reasoning
  quadratic in the fixes per collar (README, limitations).
- One extra off-schedule fix (F23, 9 July 21:30 UTC = 23:30 in Paris).
- One duplicate upload (the last CSV row repeats an F08 fix), merged by the
  Fix key through owl:sameAs.
- The precomputed values Dolfin cannot compute: `t` (Unix minutes, for time
  windows), `is_night` (local Europe/Paris hour outside 06:00-21:00), and on
  each GPX waypoint a +-0.005 deg / +-120 min search box (in <extensions>).
"""
import datetime
import math
import random
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).parent
DATA = HERE / "data"
EXPECTED = HERE / "queries" / "expected"
PARIS = ZoneInfo("Europe/Paris")
UTC = datetime.timezone.utc
START = datetime.datetime(2026, 7, 8, tzinfo=UTC)
DAYS = 5
BOX = 0.005  # degrees, ~500 m in latitude
WINDOW = 120  # minutes

random.seed(511)

# collar, name, sex, pack, collared_on, home-range centre (lat, lon)
WOLVES = [
    ("PHV-0423", "F23", "F", "NORD_VALLON", "2026-03-02", (44.300, 7.000)),
    ("PHV-0417", "M17", "M", "NORD_VALLON", "2025-11-20", (44.315, 6.980)),
    ("PHV-0531", "M31", "M", "CRETE_BLANCHE", "2026-05-14", (44.140, 7.200)),
    ("PHV-0608", "F08", "F", "CRETE_BLANCHE", "2026-06-28", (44.125, 7.215)),
]
HOME_RANGE = 0.045  # half-width of a pack's home range, in degrees

# code, kind, (min_lat, max_lat, min_lon, max_lon), grazing season or None.
# Same values as zones.dlf.
ZONES = [
    ("ALP_CABANE", "ALPAGE", (44.270, 44.285, 7.040, 7.060), ("2026-06-15", "2026-09-30")),
    ("ALP_LAUSES", "ALPAGE", (44.155, 44.165, 7.170, 7.185), ("2026-07-15", "2026-09-15")),
    ("RES_VALLON_SOMBRE", "CORE_RESERVE", (44.180, 44.240, 6.950, 7.020), None),
    ("VIL_SAINT_OURS", "VILLAGE", (44.335, 44.345, 6.990, 7.005), None),
    ("VIL_LE_PRA", "VILLAGE", (44.100, 44.108, 7.235, 7.250), None),
]

GOOD = (8, 1.2)  # satellites, hdop of a scripted fix
# Scripted alpage visits: (wolf, UTC time, zone, satellites, hdop).
SCRIPT = [
    # F23 raids the Cabane alpage on 4 nights: 5 reliable night fixes.
    ("F23", "2026-07-08T22:00", "ALP_CABANE") + GOOD,  # night 1, 00:00 local
    ("F23", "2026-07-09T21:30", "ALP_CABANE") + GOOD,  # night 2, the extra fix: 23:30 local
    ("F23", "2026-07-10T02:00", "ALP_CABANE", 5, 6.8),  # night 2, HDOP 6.8: UnreliableFix
    ("F23", "2026-07-11T00:00", "ALP_CABANE") + GOOD,  # night 3, 02:00 local
    ("F23", "2026-07-12T00:00", "ALP_CABANE") + GOOD,  # night 4, 02:00 local
    ("F23", "2026-07-12T02:00", "ALP_CABANE") + GOOD,  # night 4, 04:00 local
    ("F23", "2026-07-12T04:00", "ALP_CABANE") + GOOD,  # 06:00 local: day, not a NightFix
    # M17 comes once: 2 night fixes, under the threshold of 3.
    ("M17", "2026-07-10T20:00", "ALP_CABANE") + GOOD,  # 22:00 local (20:00 UTC reads as day)
    ("M17", "2026-07-10T22:00", "ALP_CABANE") + GOOD,  # 00:00 local
    # M31 visits the Lauses alpage before its season opens (15 July): no raid.
    ("M31", "2026-07-09T22:00", "ALP_LAUSES") + GOOD,
    ("M31", "2026-07-10T00:00", "ALP_LAUSES") + GOOD,
    ("M31", "2026-07-10T02:00", "ALP_LAUSES") + GOOD,
]
EXTRA_FIX = ("F23", "2026-07-09T21:30")  # off the 2-hour schedule
DUPLICATE = ("F08", "2026-07-11T10:00")  # uploaded twice


def utc(s):
    return datetime.datetime.fromisoformat(s).replace(tzinfo=UTC)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def minutes(t):
    return int(t.timestamp()) // 60


def is_night(t):
    hour = t.astimezone(PARIS).hour
    return hour < 6 or hour >= 21


def elevation(lat, lon):
    """A smooth invented terrain, 1100-2700 m."""
    return round(1900 + 600 * math.sin(lat * 90) * math.cos(lon * 70) + 200 * math.sin(lon * 300))


def inside(box, lat, lon, margin=0.0):
    return box[0] - margin <= lat <= box[1] + margin and box[2] - margin <= lon <= box[3] + margin


def zone(code):
    return next(z for z in ZONES if z[0] == code)


FORBIDDEN = [z[2] for z in ZONES if z[1] in ("ALPAGE", "VILLAGE")]


def walk(centre):
    """A random walk that stays in the home range and out of alpages and villages."""
    lat, lon = centre
    while True:
        nlat = lat + random.gauss(0, 0.006)
        nlon = lon + random.gauss(0, 0.006)
        if abs(nlat - centre[0]) > HOME_RANGE or abs(nlon - centre[1]) > HOME_RANGE:
            continue
        if any(inside(b, nlat, nlon, margin=0.001) for b in FORBIDDEN):
            continue
        lat, lon = nlat, nlon
        yield lat, lon


def quality():
    r = random.random()
    if r < 0.03:
        return 3, round(random.uniform(2.5, 4.0), 1)  # weak fix, consistently imprecise
    if r < 0.07:
        return random.randint(4, 6), round(random.uniform(5.5, 9.0), 1)  # HDOP > 5
    return random.randint(5, 12), round(random.uniform(0.7, 3.0), 1)


def fixes():
    """Every fix, as dicts, in upload order."""
    scripted = {(w, utc(s)): (z, sats, hdop) for w, s, z, sats, hdop in SCRIPT}
    rows = []
    for collar, name, _sex, _pack, _on, centre in WOLVES:
        steps = walk(centre)
        times = [START + datetime.timedelta(hours=2 * i) for i in range(DAYS * 12)]
        if name == EXTRA_FIX[0]:
            times.append(utc(EXTRA_FIX[1]))
            times.sort()
        for t in times:
            lat, lon = next(steps)
            sats, hdop = quality()
            if (name, t) in scripted:
                code, sats, hdop = scripted[(name, t)]
                b = zone(code)[2]
                lat = random.uniform(b[0] + 0.002, b[1] - 0.002)
                lon = random.uniform(b[2] + 0.002, b[3] - 0.002)
            rows.append(dict(collar=collar, wolf=name, t=t, lat=round(lat, 5), lon=round(lon, 5),
                             ele=elevation(lat, lon), sats=sats, hdop=hdop))
    dup = next(r for r in rows if (r["wolf"], r["t"]) == (DUPLICATE[0], utc(DUPLICATE[1])))
    rows.append(dict(dup))
    for i, r in enumerate(rows, 1):
        r["upload"] = f"U{i:05d}"
    return rows


# ----------------------------------------------------------------------------
# Ranger transect, Sunday 12 July 2026, in the Crete Blanche home range.
# ----------------------------------------------------------------------------
GPX_DAY = datetime.date(2026, 7, 12)
TRACK_START = datetime.datetime(2026, 7, 12, 5, 0, tzinfo=UTC)  # 07:00 local
TRACK_END = datetime.datetime(2026, 7, 12, 11, 0, tzinfo=UTC)  # 13:00 local
KINDS = ["SCAT", "TRACKS", "HOWL", "VISUAL"]


def near(rows, s):
    """The wolves with a fix inside the sighting's box and window."""
    return sorted({r["wolf"] for r in rows
                   if abs(r["lat"] - s["lat"]) <= BOX and abs(r["lon"] - s["lon"]) <= BOX
                   and abs(minutes(r["t"]) - minutes(s["t"])) <= WINDOW})


def sightings(rows):
    """3 sightings left by F08 60-100 min earlier, then 2 with no wolf near."""
    out = []
    morning = [r for r in rows if r["wolf"] == "F08" and r["t"].date() == GPX_DAY
               and 4 <= r["t"].hour <= 8]
    for r in morning:
        t = r["t"] + datetime.timedelta(minutes=random.randint(60, 100))
        out.append(dict(lat=round(r["lat"] + random.uniform(-0.003, 0.003), 5),
                        lon=round(r["lon"] + random.uniform(-0.003, 0.003), 5), t=t))
    out.sort(key=lambda s: s["t"])
    # The walk starts and ends at a trailhead ~900 m north of the first sign.
    base = dict(lat=round(out[0]["lat"] + 0.008, 5), lon=out[0]["lon"], t=TRACK_START)
    # The other two lie on the walk between two stops, where no wolf was.
    stops = [base] + out + [dict(base, t=TRACK_END)]
    for a, b in list(zip(stops, stops[1:])):
        while len(out) < 5:
            f = random.uniform(0.3, 0.7)
            t = a["t"] + (b["t"] - a["t"]) * f
            s = dict(lat=round(a["lat"] + f * (b["lat"] - a["lat"]), 5),
                     lon=round(a["lon"] + f * (b["lon"] - a["lon"]), 5),
                     t=t.replace(minute=t.minute - t.minute % 10, second=0, microsecond=0))
            if near(rows, s):
                break
            out.append(s)
            break
    out.sort(key=lambda s: s["t"])
    for i, s in enumerate(out, 1):
        s["name"] = f"S{i}"
        s["kind"] = KINDS[(i - 1) % len(KINDS)]
        s["ele"] = elevation(s["lat"], s["lon"])
    return out, base


def track(sights, base):
    """Track points every 10 min, walking from one sighting to the next."""
    stops = [base] + sights + [dict(base, t=TRACK_END)]
    pts = []
    t = TRACK_START
    while t <= TRACK_END:
        a = max((s for s in stops if s["t"] <= t), key=lambda s: s["t"])
        b = min((s for s in stops if s["t"] >= t), key=lambda s: s["t"])
        f = 0 if a["t"] == b["t"] else (t - a["t"]) / (b["t"] - a["t"])
        lat, lon = a["lat"] + f * (b["lat"] - a["lat"]), a["lon"] + f * (b["lon"] - a["lon"])
        pts.append(dict(lat=round(lat, 5), lon=round(lon, 5), ele=elevation(lat, lon), t=t))
        t += datetime.timedelta(minutes=10)
    return pts


def lexical(x):
    """A float as the Turtle holds it: shortest form, no trailing zeros (7.24, not 7.24000)."""
    return f"{x:.5f}".rstrip("0").rstrip(".")


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_data(rows, sights, pts):
    lines = ["upload_id,collar_id,timestamp_utc,t_min,day,lat,lon,elevation_m,satellites,hdop,is_night"]
    for r in rows:
        lines.append(f"{r['upload']},{r['collar']},{iso(r['t'])},{minutes(r['t'])},{r['t'].date()},"
                     f"{r['lat']:.5f},{r['lon']:.5f},{r['ele']},{r['sats']},{r['hdop']:.1f},"
                     f"{str(is_night(r['t'])).lower()}")
    write(DATA / "collars.csv", "\n".join(lines) + "\n")

    g = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<gpx version="1.1" creator="generate_fixes.py" xmlns="http://www.topografix.com/GPX/1/1"'
         ' xmlns:phv="https://www.dolfin.fr/showcase/wolf-tracking/gpx/1">',
         '  <metadata>',
         '    <name>Transect Crete Blanche, 2026-07-12</name>',
         '    <author><name>R-LB</name></author>',
         '  </metadata>']
    for s in sights:
        m = minutes(s["t"])
        g += [f'  <wpt lat="{s["lat"]:.5f}" lon="{s["lon"]:.5f}">',
              f'    <ele>{s["ele"]}</ele>',
              f'    <time>{iso(s["t"])}</time>',
              f'    <name>{s["name"]}</name>',
              f'    <type>{s["kind"].lower()}</type>',
              '    <extensions>',
              f'      <phv:search min_lat="{s["lat"] - BOX:.5f}" max_lat="{s["lat"] + BOX:.5f}"'
              f' min_lon="{s["lon"] - BOX:.5f}" max_lon="{s["lon"] + BOX:.5f}"'
              f' window_start="{m - WINDOW}" window_end="{m + WINDOW}"/>',
              '    </extensions>',
              '  </wpt>']
    g += ['  <trk>', '    <name>R-LB 2026-07-12</name>', '    <trkseg>']
    for p in pts:
        g += [f'      <trkpt lat="{p["lat"]:.5f}" lon="{p["lon"]:.5f}">',
              f'        <ele>{p["ele"]}</ele>',
              f'        <time>{iso(p["t"])}</time>',
              '      </trkpt>']
    g += ['    </trkseg>', '  </trk>', '</gpx>']
    write(DATA / "ranger-2026-07-12.gpx", "\n".join(g) + "\n")


# ----------------------------------------------------------------------------
# Expected query results (the rules, replayed in Python).
# ----------------------------------------------------------------------------
def expected(rows, sights, pts):
    name_of = {w[0]: w[1] for w in WOLVES}
    pack_of = {w[1]: w[3] for w in WOLVES}
    unique = {(r["wolf"], r["t"]): r for r in rows}.values()  # the duplicate is one fix

    def zones_of(r):
        return [z for z in ZONES if inside(z[2], r["lat"], r["lon"])]

    def unreliable(r):
        return r["hdop"] > 5 or r["sats"] < 4

    def raid(r, z):
        season = z[3]
        return (z[1] == "ALPAGE" and is_night(r["t"]) and not unreliable(r)
                and season[0] <= str(r["t"].date()) <= season[1])

    out = {}
    visits = sorted((iso(r["t"]), r["wolf"], z[0]) for r in unique for z in zones_of(r)
                    if z[1] == "ALPAGE" and is_night(r["t"]))
    out["night_alpage_visits"] = ["at\twolf\tzone"] + [f"{t}\t{w}\t{z}" for t, w, z in visits]

    raids = {}
    for r in unique:
        for z in zones_of(r):
            if raid(r, z):
                raids[r["wolf"]] = raids.get(r["wolf"], 0) + 1
    raiders = {w: n for w, n in raids.items() if n >= 3}
    out["alpage_raiders"] = ["wolf\traid_fixes"] + [f"{w}\t{n}" for w, n in sorted(raiders.items())]

    lines = ["wolf\tuploads\tfixes\tdays"]
    for w in sorted(name_of.values()):
        mine = [r for r in rows if r["wolf"] == w]
        lines.append(f"{w}\t{len(mine)}\t{len({r['t'] for r in mine})}\t{len({r['t'].date() for r in mine})}")
    out["fixes_per_wolf"] = lines

    prof = []
    for w in name_of.values():
        e = [r["ele"] for r in rows if r["wolf"] == w]
        prof.append((max(e), min(e), w))
    out["elevation_profile"] = ["wolf\tlowest\thighest"] + [f"{w}\t{lo}\t{hi}" for hi, lo, w in sorted(prof, reverse=True)]

    out["unconfirmed_sightings"] = ["sighting\tkind\tat"] + [
        f"{s['name']}\tSightingKind_{s['kind']}\t{iso(s['t'])}" for s in sights if not near(rows, s)]
    out["ranger_track"] = ["at\tlat\tlon"] + [f"{iso(p['t'])}\t{lexical(p['lat'])}\t{lexical(p['lon'])}" for p in pts[:20]]

    problem = {pack_of[w] for w in raiders}
    lines = ["pack\tnight_fixes"]
    for p in sorted(problem):
        n = sum(1 for r in unique if pack_of[r["wolf"]] == p and is_night(r["t"]))
        lines.append(f"{p}\t{n}")
    out["pack_activity"] = lines
    return out


def main():
    rows = fixes()
    sights, base = sightings(rows)
    pts = track(sights, base)
    if "--print-expected" in sys.argv:
        EXPECTED.mkdir(parents=True, exist_ok=True)
        for name, lines in expected(rows, sights, pts).items():
            write(EXPECTED / f"{name}.tsv", "\n".join(lines) + "\n")
            print(f"--- {name}.tsv\n" + "\n".join(lines))
        return
    DATA.mkdir(exist_ok=True)
    write_data(rows, sights, pts)
    print(f"wrote {len(rows)} collar rows, {len(sights)} waypoints, {len(pts)} track points")


if __name__ == "__main__":
    main()
