import unittest
from ecotracker.storage import MeasurementStorage


class TestStorage(unittest.TestCase):
    """FR-1 и FR-2: приём и хранение измерений."""

    def setUp(self):
        self.db = MeasurementStorage()
        self.db.add("ST-01", "PM2.5", 12.5, "2026-11-01T10:00:00")
        self.db.add("ST-01", "PM10", 40, "2026-11-01T10:00:00")
        self.db.add("ST-02", "PM2.5", 30, "2026-11-02T10:00:00")

    def test_count(self):
        self.assertEqual(self.db.count(), 3)

    def test_filter_by_station(self):
        self.assertEqual(len(self.db.get(station="ST-01")), 2)

    def test_filter_by_pollutant(self):
        self.assertEqual(len(self.db.get(pollutant="PM2.5")), 2)

    def test_filter_since(self):
        self.assertEqual(len(self.db.get(since="2026-11-02T00:00:00")), 1)

    def test_invalid_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            self.db.add("ST-01", "PM2.5", 5, "вчера")

    def test_negative_value_rejected(self):
        with self.assertRaises(ValueError):
            self.db.add("ST-01", "PM2.5", -5, "2026-11-03T10:00:00")

    def test_empty_station_rejected(self):
        with self.assertRaises(ValueError):
            self.db.add("  ", "PM2.5", 5, "2026-11-03T10:00:00")

    def test_rejected_record_not_saved(self):
        try:
            self.db.add("ST-01", "PM2.5", -1, "2026-11-03T10:00:00")
        except ValueError:
            pass
        self.assertEqual(self.db.count(), 3)


if __name__ == "__main__":
    unittest.main()
