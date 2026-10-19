import sys
from .ingest import load_records
from .core import summarize
from .delivery import publish

def main(path):
    summary = summarize(load_records(path))
    publish(summary)
    return summary["total_cents"]

if __name__ == "__main__":
    print(main(sys.argv[1]))
