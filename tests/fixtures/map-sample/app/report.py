from app.core import load_records


def write_report(path, out_path):
    records = load_records(path)
    with open(out_path, "w") as f:
        f.write("\n".join(str(r["id"]) for r in records))
