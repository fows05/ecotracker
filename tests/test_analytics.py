import unittest
from ecotracker.analytics import calc_aqi, aqi_category, average


class TestAnalytics(unittest.TestCase):
    """FR-3: расчёт индекса качества воздуха."""

    def test_pm25_good_upper_bound(self):
        self.assertEqual(calc_aqi("PM2.5", 12.0), 50)

    def test_pm25_moderate(self):
        self.assertEqual(calc_aqi("PM2.5", 35.4), 100)

    def test_pm25_zero(self):
        self.assertEqual(calc_aqi("PM2.5", 0), 0)

    def test_pm10_values(self):
        self.assertEqual(calc_aqi("PM10", 54), 50)
        self.assertEqual(calc_aqi("PM10", 154), 100)

    def test_above_scale_returns_500(self):
        self.assertEqual(calc_aqi("PM10", 1000), 500)

    def test_negative_value_rejected(self):
        with self.assertRaises(ValueError):
            calc_aqi("PM2.5", -1)

    def test_unknown_pollutant_rejected(self):
        with self.assertRaises(ValueError):
            calc_aqi("XYZ", 10)

    def test_categories(self):
        self.assertEqual(aqi_category(25), "Хорошо")
        self.assertEqual(aqi_category(100), "Умеренно")
        self.assertEqual(aqi_category(180), "Вредно")
        self.assertEqual(aqi_category(450), "Опасно")

    def test_average(self):
        self.assertEqual(average([10, 20, 30]), 20)

    def test_average_empty_rejected(self):
        with self.assertRaises(ValueError):
            average([])


if __name__ == "__main__":
    unittest.main()
