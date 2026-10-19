def summarize(records):
    rows = list(records)
    return {"count": len(rows), "total_cents": sum(row["amount_cents"] for row in rows)}
