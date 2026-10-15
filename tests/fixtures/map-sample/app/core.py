import csv


def load_records(path):
    """Read invoices, sorted by id. Amount is parsed as float."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: r["id"])
    for r in rows:
        r["amount"] = float(r["amount"])
    return rows


def summarize(records):
    total = sum(r["amount"] for r in records)
    return [f"count={len(records)}", f"total={total:.2f}"]
