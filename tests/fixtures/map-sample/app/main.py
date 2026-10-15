import sys

from app.core import load_records, summarize


def main(argv=None):
    path = (argv or sys.argv[1:])[0]
    records = load_records(path)
    for line in summarize(records):
        print(line)


if __name__ == "__main__":
    main()
