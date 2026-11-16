# /// script
# dependencies = ["openpyxl"]
# ///
"""Generate data/exchanges.xlsx, the cooperative's exchange book, once.

    uv run generate_exchanges.py

The Dolfin package only reads the resulting file (mappings.dlf); this script
is not part of the build. The exchanges are written out below, and the giver
of each is the lot's holder in data/lots.csv. Re-running it writes the same
bytes: the workbook's creation time and the zip entries' times are pinned.
"""
import csv
import datetime
import re
import zipfile
from pathlib import Path

from openpyxl import Workbook

DATA = Path(__file__).parent / "data"
OUT = DATA / "exchanges.xlsx"
PINNED = datetime.datetime(2026, 6, 1)

# (date, lot, receiving farm's SIRET, price in graines or None for a gift)
EXCHANGES = [
    ("2025-01-18", "GV-2024-003", "82100445600017", 6),
    ("2025-02-08", "GV-2024-005", "82101045600017", 4),
    ("2025-02-22", "GV-2024-004", "82101245600017", 5),
    ("2025-03-15", "GV-2024-010", "82100945600017", 8),
    ("2025-03-15", "GV-2024-001", "82100745600017", 10),
    ("2025-04-05", "GV-2024-007", "82101345600017", None),
    ("2025-04-26", "GV-2024-006", "82100145600017", 3),
    ("2025-05-10", "GV-2023-002", "82101145600017", 4),
    ("2025-06-07", "GV-2024-002", "82101345600017", 2),
    ("2025-06-21", "GV-2024-011", "82100245600017", 12),
    ("2025-07-05", "GV-2025-003", "82100845600017", 7),
    ("2025-07-19", "GV-2023-003", "82100645600017", 5),
    ("2025-08-30", "GV-2025-008", "82100545600017", 3),
    ("2025-09-13", "GV-2025-001", "82101245600017", 9),
    ("2025-09-27", "GV-2024-009", "82101545600017", None),  # welcome gift to the newest member
    ("2025-10-11", "GV-2025-007", "82100945600017", 15),
    ("2025-10-25", "GV-2025-004", "82100345600017", 4),
    ("2025-11-08", "GV-2025-011", "82100645600017", 3),
    ("2025-11-22", "GV-2025-018", "82100245600017", 6),
    ("2025-12-06", "GV-2025-015", "82101145600017", 10),
    ("2026-01-17", "GV-2025-009", "82100145600017", 5),
    ("2026-01-31", "GV-2025-002", "82100545600017", 4),
    ("2026-02-14", "GV-2025-013", "82100345600017", 3),
    ("2026-02-28", "GV-2025-024", "82100445600017", 12),
    ("2026-03-14", "GV-2025-021", "82101245600017", 6),
    ("2026-03-28", "GV-2025-005", "82101045600017", 14),
    ("2026-04-11", "GV-2025-010", "82101545600017", 4),
    ("2026-04-25", "GV-2025-027", "82100845600017", 5),
    ("2026-05-09", "GV-2025-028", "82100145600017", 7),
    ("2026-05-23", "GV-2025-002", "82101445600017", 4.5),
]

with open(DATA / "lots.csv", newline="", encoding="utf-8") as f:
    holder = {r["lot_id"]: r["holder_siret"] for r in csv.DictReader(f)}

wb = Workbook()
wb.properties.creator = "Graines du Vercors"
wb.properties.created = wb.properties.modified = PINNED
ws = wb.active
ws.title = "Exchanges"
ws.append(["exchange_id", "date", "from_siret", "to_siret", "lot_id", "price"])
for n, (date, lot, to, price) in enumerate(EXCHANGES, 1):
    assert holder[lot] != to, f"exchange {n}: {lot} given to its own holder"
    ws.append([f"E{n:03d}", datetime.date.fromisoformat(date), holder[lot], to, lot, price])
ws.column_dimensions["B"].width = 12
wb.save(OUT)

# openpyxl stamps the zip entries and `dcterms:modified` with the current
# time on save: rewrite them pinned.
with zipfile.ZipFile(OUT) as z:
    entries = [(i.filename, z.read(i)) for i in z.infolist()]
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in entries:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*", rb"\g<1>2026-06-01T00:00:00Z", data)
        z.writestr(zipfile.ZipInfo(name, PINNED.timetuple()[:6]), data, zipfile.ZIP_DEFLATED)
print(f"wrote {OUT}: {len(EXCHANGES)} exchanges")
