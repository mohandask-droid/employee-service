import csv
import json
import logging
from pathlib import Path

import pymupdf
from openpyxl import Workbook, load_workbook

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE = Path(__file__).parent


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["salary"] = int(r["salary"])
    return rows


def read_file(path: str | Path) -> str | None:
    try:
        text = Path(path).read_text()
        if str(path).endswith(".json"):
            json.loads(text)
        return text
    except FileNotFoundError:
        logger.error("File not found: %s", path)
    except json.JSONDecodeError:
        logger.error("Invalid JSON: %s", path)
    return None


def find_employee(name: str) -> dict | None:
    for e in read_csv(BASE / "employees.csv"):
        if e["name"].lower() == name.lower():
            return e
    return None


if __name__ == "__main__":
    emps = read_csv(BASE / "employees.csv")

    (BASE / "employees.json").write_text(json.dumps(emps, indent=2))

    high = [e for e in emps if e["salary"] > 50000]
    with (BASE / "high_earners.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
        w.writeheader()
        w.writerows(high)
    print(f"Rows read: {len(emps)} | High earners written: {len(high)}")

    wb = Workbook()
    ws = wb.active
    ws.append(["name", "department", "salary"])
    for e in emps:
        ws.append([e["name"], e["department"], e["salary"]])
    wb.save(BASE / "salary.xlsx")
    rows = load_workbook(BASE / "salary.xlsx").active.max_row - 1
    print(f"salary.xlsx created and read back: {rows} rows")

    pdf = BASE / "sample.pdf"
    if pdf.exists():
        print(pymupdf.open(pdf)[0].get_text()[:100])
    else:
        logger.error("File not found: sample.pdf")

    read_file("missing.txt")
