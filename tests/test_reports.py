import csv
import os
import tempfile
import unittest
from ecotracker.reports import export_csv


class TestReports(unittest.TestCase):
    """FR-6: формирование отчёта."""

    def test_export_csv(self):
        rows = [("ST-01", "PM2.5", 12.5, "2026-11-01T10:00:00"),
                ("ST-02", "PM10", 40.0, "2026-11-02T10:00:00")]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "report.csv")
            self.assertEqual(export_csv(rows, path), 2)
            with open(path, encoding="utf-8") as f:
                data = list(csv.reader(f))
        self.assertEqual(data[0], ["station", "pollutant", "value", "timestamp"])
        self.assertEqual(len(data), 3)

    def test_export_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(export_csv([], os.path.join(d, "r.csv")), 0)


if __name__ == "__main__":
    unittest.main()
