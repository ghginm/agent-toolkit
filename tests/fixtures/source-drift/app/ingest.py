import csv
from decimal import Decimal

def load_records(path):
    """Yield invoices in file order. No deduplication is performed."""
    with open(path, newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            yield {"id": row["id"], "amount_cents": int(Decimal(row["amount"]) * 100)}
