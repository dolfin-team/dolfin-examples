# /// script
# dependencies = ["openpyxl"]
# ///
"""Generate data/marks.xlsx, the term's gradebook, once.

    uv run generate_marks.py

Reads the classes and students from data/*.csv so the workbook matches them.
The Dolfin package only reads the resulting file (marks.dlf); this script is
not part of the build. Seeded: re-running it writes the same marks.
"""
import csv
import datetime
import random
from pathlib import Path

from openpyxl import Workbook

DATA = Path(__file__).parent / "data"
SUBJECTS = ["MATH", "FRENCH", "HISTGEO", "ENGLISH", "PHYSCHEM", "BIOLOGY", "PE"]
TERM_START = datetime.date(2026, 9, 7)
TERM_WEEKS = 15
ABSENT = "ABS"

random.seed(2026)


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


classes = [c["code"] for c in read("classes.csv")]
students = read("students.csv")
ability = {s["id"]: random.gauss(11, 2.5) for s in students}

wb = Workbook()
tests_ws = wb.active
tests_ws.title = "Tests"
tests_ws.append(["test_id", "date", "class", "subject", "title"])

marks_ws = wb.create_sheet("Marks")
# A banner above the table, as teachers' gradebooks have: the mapping says `header row 3`.
marks_ws.append(["Relevé de notes — 1er trimestre 2026-2027"])
marks_ws.append([])
marks_ws.append(["test_id", "student_id", "mark"])

n = 0
for cls in classes:
    members = [s["id"] for s in students if s["class"] == cls]
    for subject in SUBJECTS:
        for k in (1, 2):
            n += 1
            test_id = f"E{n:03d}"
            week = random.randrange(TERM_WEEKS) if k == 1 else random.randrange(TERM_WEEKS // 2, TERM_WEEKS)
            date = TERM_START + datetime.timedelta(weeks=week, days=random.randrange(5))
            tests_ws.append([test_id, date, cls, subject, f"Évaluation {k}"])
            for sid in members:
                if random.random() < 0.06:
                    mark = ABSENT
                else:
                    # French marks: out of 20, to the half point.
                    mark = min(20, max(0, round(random.gauss(ability[sid], 3) * 2) / 2))
                marks_ws.append([test_id, sid, mark])

tests_ws.column_dimensions["B"].width = 12
wb.save(DATA / "marks.xlsx")
print(f"wrote {DATA / 'marks.xlsx'}: {n} tests, {marks_ws.max_row - 3} marks")
