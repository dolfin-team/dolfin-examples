# /// script
# dependencies = ["openpyxl"]
# ///
"""Generate data/scolarite.xlsx, the school office's workbook, once.

    uv run generate_scolarite.py

Reads the UEs from data/ue.csv. Writes three sheets:
  Notes        one mark out of 20 per student and UE (the table below)
  Pondération  one row per coefficient point of each UE (see scolarite.dlf)
  Séances      the teaching sessions, one row per session
The Dolfin package only reads the resulting file (mappings.dlf); this script
is not part of the build and writes the same file every time.
"""
import csv
import datetime
from pathlib import Path

from openpyxl import Workbook

DATA = Path(__file__).parent / "data"

# Marks, in the order of data/ue.csv: MATH1 ALGO1 ANGL1 | PROBA2 BDD2 COMM2.
# E26009 is on a two-year plan: she takes MATH1, ANGL1 and PROBA2 this year.
MARKS = {
    "E26001": [14, 12, 15, 13, 11, 12],
    "E26002": [11, 8, 13, 12, 10, 9],
    "E26003": [7, 9, 12, 8, 6, 11],
    "E26004": [16, 17, 14, 15, 16, 18],
    "E26005": [10, 10, 10, 9.5, 12, 11],
    "E26006": [13, 7, 7, 11, 9, 10],
    "E26007": [9, 12, 16, 14, 13, 15],
    "E26008": [8, 10, 8, 10, 10, 12],
    "E26009": [12, None, 14, 11, None, None],
}
# Hours actually taught per UE, in sessions of this many hours. MATH1 is over
# its planned 60 h (64 h), BDD2 under its planned 40 h (36 h).
SESSIONS = {"MATH1": (16, 4), "ALGO1": (12, 4), "ANGL1": (12, 2),
            "PROBA2": (12, 4), "BDD2": (9, 4), "COMM2": (10, 2)}
START = {"S1": datetime.date(2026, 9, 14), "S2": datetime.date(2027, 1, 18)}

with open(DATA / "ue.csv", newline="", encoding="utf-8") as f:
    ues = list(csv.DictReader(f))

wb = Workbook()
notes = wb.active
notes.title = "Notes"
notes.append(["etudiant", "ue", "note"])
for student, marks in MARKS.items():
    for ue, mark in zip(ues, marks):
        if mark is not None:
            notes.append([student, ue["code"], mark])

weights = wb.create_sheet("Pondération")
weights.append(["ue", "part"])
for ue in ues:
    for part in range(1, int(ue["coefficient"]) + 1):
        weights.append([ue["code"], part])

sessions = wb.create_sheet("Séances")
sessions.append(["id", "enseignant", "ue", "date", "duree_h"])
n = 0
for ue in ues:
    count, hours = SESSIONS[ue["code"]]
    for k in range(count):
        n += 1
        sessions.append([f"S{n:03d}", ue["enseignant"], ue["code"],
                         START[ue["semestre"]] + datetime.timedelta(weeks=k % 12, days=k // 12), hours])
sessions.column_dimensions["D"].width = 12
wb.save(DATA / "scolarite.xlsx")
print(f"wrote {DATA / 'scolarite.xlsx'}: {notes.max_row - 1} marks, {n} sessions")
