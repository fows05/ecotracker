"""Оповещения о превышении ПДК. Требование FR-4."""

# Предельные значения, мкг/м3 (учебные; сверяйтесь с действующим СанПиН)
PDK = {"PM2.5": 35.0, "PM10": 60.0}


def check_pdk(pollutant, value, limits=None):
    """True, если концентрация превышает ПДК."""
    limits = PDK if limits is None else limits
    if pollutant not in limits:
        raise ValueError("Для загрязнителя %s не задан ПДК" % pollutant)
    return value > limits[pollutant]


def make_alert(station, pollutant, value):
    """Формирует оповещение или возвращает None, если превышения нет."""
    if not check_pdk(pollutant, value):
        return None
    return {"station": station, "pollutant": pollutant, "value": value,
            "limit": PDK[pollutant],
            "message": "Превышение ПДК %s на станции %s: %s мкг/м3 (ПДК %s)"
                       % (pollutant, station, value, PDK[pollutant])}
