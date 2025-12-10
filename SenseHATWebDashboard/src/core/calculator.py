# Calculation logic

def pressure_to_altitude(pressure, sea_level_pressure=1013.25):
    """
    Converts atmospheric pressure to altitude.

    :param pressure: Current atmospheric pressure in hPa.
    :param sea_level_pressure: Atmospheric pressure at sea level in hPa.
    :return: Altitude in meters.
    """
    return 44330 * (1 - (pressure / sea_level_pressure) ** (1 / 5.255))