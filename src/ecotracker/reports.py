"""Формирование отчётов. Требование FR-6."""
import csv


def export_csv(measurements, path):
    """Записывает измерения в CSV-файл и возвращает число строк данных."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["station", "pollutant", "value", "timestamp"])
        w.writerows(measurements)
    return len(measurements)
