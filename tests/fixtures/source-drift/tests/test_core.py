import unittest
from app.core import summarize

class CoreTests(unittest.TestCase):
    def test_duplicate_ids_are_counted(self):
        self.assertEqual(summarize([{ "id": "1", "amount_cents": 125}] * 2),
                         {"count": 2, "total_cents": 250})
