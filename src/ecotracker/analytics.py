"""Аналитика: расчёт индекса качества воздуха (AQI). Требование FR-3."""
import math

# Пороги по методике EPA (учебная модель): (c_low, c_high, aqi_low, aqi_high)
BREAKPOINTS = {
    "PM2.5": [(0.0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
              (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300),
              (250.5, 350.4, 301, 400), (350.5, 500.4, 401, 500)],
    "PM10": [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150),
             (255, 354, 151, 200), (355, 424, 201, 300),
             (425, 504, 301, 400), (505, 604, 401, 500)],
}


def calc_aqi(pollutant, value):
    """Возвращает индекс AQI (целое 0..500) для загрязнителя и концентрации, мкг/м3."""
    if pollutant not in BREAKPOINTS:
        raise ValueError("Неизвестный загрязнитель: %s" % pollutant)
    if value < 0:
        raise ValueError("Концентрация не может быть отрицательной")
    # Усечение концентрации по правилам методики
    value = math.floor(value * 10) / 10 if pollutant == "PM2.5" else math.floor(value)
    table = BREAKPOINTS[pollutant]
    if value > table[-1][1]:
        return 500
    for c_lo, c_hi, i_lo, i_hi in table:
        if c_lo <= value <= c_hi:
            return round((i_hi - i_lo) / (c_hi - c_lo) * (value - c_lo) + i_lo)
    raise ValueError("Концентрация вне диапазона таблицы")


def aqi_category(aqi):
    """Словесная категория качества воздуха по значению AQI."""
    if aqi < 0:
        raise ValueError("AQI не может быть отрицательным")
    for upper, name in [(50, "Хорошо"), (100, "Умеренно"),
                        (150, "Вредно для чувствительных групп"),
                        (200, "Вредно"), (300, "Очень вредно")]:
        if aqi <= upper:
            return name
    return "Опасно"


def average(values):
    """Среднее значение ряда измерений."""
    if not values:
        raise ValueError("Пустой ряд измерений")
    return sum(values) / len(values)
