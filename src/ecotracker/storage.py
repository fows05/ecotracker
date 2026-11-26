"""Приём и хранение измерений (SQLite). Требования FR-1 и FR-2."""
import sqlite3
from datetime import datetime


class MeasurementStorage:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS measurements ("
                          "station TEXT NOT NULL, pollutant TEXT NOT NULL, "
                          "value REAL NOT NULL, ts TEXT NOT NULL)")

    def add(self, station, pollutant, value, ts):
        """Проверяет и сохраняет одно измерение (ts - строка ISO 8601)."""
        if not station or not str(station).strip():
            raise ValueError("Не указана станция")
        if not pollutant:
            raise ValueError("Не указан загрязнитель")
        if value < 0:
            raise ValueError("Значение не может быть отрицательным")
        datetime.fromisoformat(ts)  # ValueError при неверном формате
        self.conn.execute("INSERT INTO measurements VALUES (?,?,?,?)",
                          (station, pollutant, float(value), ts))
        self.conn.commit()

    def get(self, station=None, pollutant=None, since=None):
        """Возвращает список измерений (station, pollutant, value, ts) по фильтрам."""
        sql, args = "SELECT station, pollutant, value, ts FROM measurements WHERE 1=1", []
        if station:
            sql += " AND station=?"
            args.append(station)
        if pollutant:
            sql += " AND pollutant=?"
            args.append(pollutant)
        if since:
            sql += " AND ts>=?"
            args.append(since)
        return self.conn.execute(sql + " ORDER BY ts", args).fetchall()

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
