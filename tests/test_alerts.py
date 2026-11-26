import unittest
from ecotracker.alerts import check_pdk, make_alert


class TestAlerts(unittest.TestCase):
    """FR-4: оповещение о превышении ПДК."""

    def test_below_limit(self):
        self.assertFalse(check_pdk("PM2.5", 20))

    def test_equal_to_limit_is_not_exceeded(self):
        self.assertFalse(check_pdk("PM2.5", 35.0))

    def test_above_limit(self):
        self.assertTrue(check_pdk("PM10", 61))

    def test_unknown_pollutant(self):
        with self.assertRaises(ValueError):
            check_pdk("XYZ", 5)

    def test_alert_created_on_exceed(self):
        alert = make_alert("ST-01", "PM2.5", 50)
        self.assertEqual(alert["station"], "ST-01")
        self.assertIn("Превышение ПДК", alert["message"])

    def test_no_alert_when_normal(self):
        self.assertIsNone(make_alert("ST-01", "PM2.5", 10))


if __name__ == "__main__":
    unittest.main()
