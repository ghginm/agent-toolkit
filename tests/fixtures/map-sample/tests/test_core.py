from app.core import load_records, summarize


def test_summarize(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("id,amount\n2,10.5\n1,4.5\n")
    recs = load_records(str(p))
    assert [r["id"] for r in recs] == ["1", "2"]
    assert summarize(recs) == ["count=2", "total=15.00"]
